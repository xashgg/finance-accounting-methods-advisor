"""
DoubleML starter for PLR or IRM designs.

This is estimation scaffolding, not an identification strategy.

PLR:
    Y = theta D + g(X) + error
    Suitable for a partially linear causal model under its assumptions.

IRM:
    Binary treatment under unconfoundedness/overlap assumptions.

If --group-column is supplied, GroupKFold is used to define external
cross-fitting folds so that groups (e.g., firms) do not cross folds.
"""

from __future__ import annotations

import argparse
import platform
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.model_selection import GroupKFold

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
    p.add_argument("--outcome", required=True)
    p.add_argument("--treatment", required=True)
    p.add_argument("--covariates", nargs="+", required=True)
    p.add_argument(
        "--design",
        choices=["plr", "irm"],
        default="plr",
        help="IRM requires binary treatment.",
    )
    p.add_argument("--group-column")
    p.add_argument("--n-folds", type=int, default=5)
    p.add_argument("--n-trees", type=int, default=500)
    p.add_argument("--min-samples-leaf", type=int, default=10)
    p.add_argument("--random-state", type=int, default=42)
    p.add_argument("--output-dir", required=True)
    return p.parse_args()


def group_splits(df, group_col, n_folds):
    groups = df[group_col].to_numpy()
    splitter = GroupKFold(n_splits=n_folds)
    dummy_x = np.zeros((len(df), 1))
    return [(train, test) for train, test in splitter.split(dummy_x, groups=groups)]


def main():
    args = parse_args()

    try:
        import doubleml as dml
    except ImportError as exc:
        raise SystemExit("Install doubleml before running this script.") from exc

    required = [args.outcome, args.treatment, *args.covariates]
    if args.group_column:
        required.append(args.group_column)

    df = read_table(args.input)
    require_columns(df, required)
    df = df[required].dropna().reset_index(drop=True)

    if args.design == "irm":
        treatment_values = set(pd.unique(df[args.treatment]))
        if not treatment_values.issubset({0, 1, False, True}):
            raise ValueError("IRM requires a binary 0/1 treatment.")

    output_dir = ensure_output_dir(args.output_dir)

    data = dml.DoubleMLData(
        df,
        y_col=args.outcome,
        d_cols=args.treatment,
        x_cols=args.covariates,
    )

    rf_reg = RandomForestRegressor(
        n_estimators=args.n_trees,
        min_samples_leaf=args.min_samples_leaf,
        random_state=args.random_state,
        n_jobs=-1,
    )
    rf_clf = RandomForestClassifier(
        n_estimators=args.n_trees,
        min_samples_leaf=args.min_samples_leaf,
        random_state=args.random_state,
        n_jobs=-1,
        class_weight="balanced",
    )

    draw_internal = args.group_column is None

    if args.design == "plr":
        # For binary treatment, DoubleMLPLR can use a classifier for m(X).
        binary_treatment = set(pd.unique(df[args.treatment])).issubset(
            {0, 1, False, True}
        )
        ml_m = rf_clf if binary_treatment else rf_reg
        model = dml.DoubleMLPLR(
            data,
            ml_l=rf_reg,
            ml_m=ml_m,
            n_folds=args.n_folds,
            draw_sample_splitting=draw_internal,
        )
    else:
        model = dml.DoubleMLIRM(
            data,
            ml_g=rf_reg,
            ml_m=rf_clf,
            n_folds=args.n_folds,
            draw_sample_splitting=draw_internal,
        )

    if args.group_column:
        smpls = group_splits(df, args.group_column, args.n_folds)
        model.set_sample_splitting(smpls)

    model.fit()

    summary = model.summary.copy()
    summary.to_csv(output_dir / "dml_summary.csv")

    # Preserve the actual split indices when available.
    split_rows = []
    for fold, (train_idx, test_idx) in enumerate(model.smpls[0], start=1):
        for idx in train_idx:
            split_rows.append({"fold": fold, "row": int(idx), "role": "train"})
        for idx in test_idx:
            split_rows.append({"fold": fold, "row": int(idx), "role": "test"})
    write_table(pd.DataFrame(split_rows), output_dir / "crossfit_splits")

    write_json(
        output_dir / "manifest.json",
        {
            "created_utc": utc_now_iso(),
            "input": str(Path(args.input).resolve()),
            "design": args.design,
            "outcome": args.outcome,
            "treatment": args.treatment,
            "covariates": args.covariates,
            "n_obs_complete_case": len(df),
            "n_folds": args.n_folds,
            "group_column": args.group_column,
            "learner": "RandomForest",
            "n_trees": args.n_trees,
            "min_samples_leaf": args.min_samples_leaf,
            "random_state": args.random_state,
            "python": platform.python_version(),
            "doubleml": getattr(dml, "__version__", "unknown"),
            "research_warning": (
                "DML does not solve endogenous treatment or unobserved confounding. "
                "Identification assumptions, treatment timing, overlap, and appropriate "
                "inference/clustering must be justified separately."
            ),
        },
    )

    print(summary)
    print(f"Outputs saved to {output_dir}")


if __name__ == "__main__":
    main()
