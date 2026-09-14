"""
Leakage-aware baseline text classifier.

Requires a pre-existing split column with train/valid/test labels.
This is intentional: finance/accounting projects often require firm-grouped or
temporal splits that should be designed before model fitting.
"""

from __future__ import annotations

import argparse
import platform
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from _io_utils import (
    ensure_output_dir,
    read_table,
    require_columns,
    utc_now_iso,
    write_json,
    write_table,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--id-column", required=True)
    p.add_argument("--text-column", required=True)
    p.add_argument("--label-column", required=True)
    p.add_argument("--split-column", required=True)
    p.add_argument("--train-value", default="train")
    p.add_argument("--valid-value", default="valid")
    p.add_argument("--test-value", default="test")
    p.add_argument(
        "--model",
        choices=["logit", "linear-svm"],
        default="logit",
    )
    p.add_argument("--min-df", type=int, default=5)
    p.add_argument("--max-features", type=int, default=100_000)
    p.add_argument("--output-dir", required=True)
    return p.parse_args()


def build_pipeline(args):
    tfidf = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=args.min_df,
        max_df=0.95,
        max_features=args.max_features,
        sublinear_tf=True,
    )

    if args.model == "logit":
        estimator = LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
        )
    else:
        estimator = LinearSVC(class_weight="balanced")

    return Pipeline([("tfidf", tfidf), ("model", estimator)])


def evaluate(model, frame, args, split_name, output_dir):
    y_true = frame[args.label_column]
    y_pred = model.predict(frame[args.text_column])

    report = classification_report(
        y_true,
        y_pred,
        output_dict=True,
        zero_division=0,
    )
    write_json(output_dir / f"{split_name}_classification_report.json", report)

    labels = sorted(pd.unique(pd.concat([y_true, pd.Series(y_pred)]).astype(str)))
    cm = confusion_matrix(
        y_true.astype(str),
        pd.Series(y_pred).astype(str),
        labels=labels,
    )
    pd.DataFrame(cm, index=labels, columns=labels).to_csv(
        output_dir / f"{split_name}_confusion_matrix.csv"
    )

    preds = frame[[args.id_column, args.label_column]].copy()
    preds["prediction"] = y_pred
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(frame[args.text_column])
        classes = model.named_steps["model"].classes_
        for j, cls in enumerate(classes):
            preds[f"prob_{cls}"] = proba[:, j]
    write_table(preds, output_dir / f"{split_name}_predictions")

    return report


def main():
    args = parse_args()
    df = read_table(args.input)
    require_columns(
        df,
        [
            args.id_column,
            args.text_column,
            args.label_column,
            args.split_column,
        ],
    )

    if df[args.id_column].duplicated().any():
        raise ValueError("ID column must be unique.")

    df = df.copy()
    df[args.text_column] = df[args.text_column].fillna("").astype(str)

    split_values = {
        "train": args.train_value,
        "valid": args.valid_value,
        "test": args.test_value,
    }
    frames = {
        name: df[df[args.split_column] == value].copy()
        for name, value in split_values.items()
    }

    empty = [name for name, frame in frames.items() if frame.empty]
    if empty:
        raise ValueError(f"Empty required splits: {empty}")

    output_dir = ensure_output_dir(args.output_dir)
    model = build_pipeline(args)
    model.fit(frames["train"][args.text_column], frames["train"][args.label_column])

    valid_report = evaluate(model, frames["valid"], args, "valid", output_dir)
    test_report = evaluate(model, frames["test"], args, "test", output_dir)

    joblib.dump(model, output_dir / "model.joblib")

    write_json(
        output_dir / "manifest.json",
        {
            "created_utc": utc_now_iso(),
            "input": str(Path(args.input).resolve()),
            "model": args.model,
            "n_train": len(frames["train"]),
            "n_valid": len(frames["valid"]),
            "n_test": len(frames["test"]),
            "split_column": args.split_column,
            "split_values": split_values,
            "python": platform.python_version(),
            "sklearn": sklearn.__version__,
            "valid_macro_f1": valid_report.get("macro avg", {}).get("f1-score"),
            "test_macro_f1": test_report.get("macro avg", {}).get("f1-score"),
            "research_note": (
                "Confirm that the supplied split prevents firm, temporal, template, "
                "and near-duplicate leakage. Report class-level metrics, not accuracy alone."
            ),
        },
    )

    print(f"Classifier outputs saved to {output_dir}")


if __name__ == "__main__":
    main()
