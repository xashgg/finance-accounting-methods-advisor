"""
Classical NMF + optional BERTopic topic-discovery starter pipeline.

Do not interpret an algorithmic topic count as the unique true number of
economic/accounting constructs. Use outputs for stability and human review.
"""

from __future__ import annotations

import argparse
import platform
from pathlib import Path

import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

from _io_utils import (
    ensure_output_dir,
    read_table,
    require_columns,
    text_sha256,
    utc_now_iso,
    write_json,
    write_table,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--id-column", required=True)
    p.add_argument("--text-column", required=True)
    p.add_argument(
        "--mode",
        choices=["nmf", "bertopic", "both"],
        default="both",
    )
    p.add_argument("--nmf-topics", type=int, default=20)
    p.add_argument("--top-words", type=int, default=15)
    p.add_argument("--min-df", type=int, default=5)
    p.add_argument("--max-features", type=int, default=100_000)
    p.add_argument(
        "--embedding-model",
        default="sentence-transformers/all-MiniLM-L6-v2",
    )
    p.add_argument("--min-cluster-size", type=int, default=15)
    p.add_argument("--umap-neighbors", type=int, default=15)
    p.add_argument("--random-state", type=int, default=42)
    p.add_argument("--output-dir", required=True)
    return p.parse_args()


def run_nmf(df, text_col, id_col, args, output_dir):
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=args.min_df,
        max_df=0.95,
        max_features=args.max_features,
    )
    X = vectorizer.fit_transform(df[text_col])

    model = NMF(
        n_components=args.nmf_topics,
        init="nndsvda",
        random_state=args.random_state,
        max_iter=500,
    )
    doc_topic = model.fit_transform(X)
    feature_names = vectorizer.get_feature_names_out()

    topic_rows = []
    for k, weights in enumerate(model.components_):
        top_idx = weights.argsort()[::-1][: args.top_words]
        topic_rows.append(
            {
                "topic": k,
                "top_terms": " | ".join(feature_names[top_idx]),
            }
        )
    pd.DataFrame(topic_rows).to_csv(
        output_dir / "nmf_topic_terms.csv", index=False
    )

    assignment = df[[id_col]].copy()
    assignment["nmf_topic"] = doc_topic.argmax(axis=1)
    assignment["nmf_topic_weight"] = doc_topic.max(axis=1)
    write_table(assignment, output_dir / "nmf_document_topics")

    return {
        "n_topics": args.nmf_topics,
        "n_features": int(X.shape[1]),
        "reconstruction_error": float(model.reconstruction_err_),
    }


def run_bertopic(df, text_col, id_col, args, output_dir):
    try:
        import bertopic
        import hdbscan
        import sentence_transformers
        import umap
        from bertopic import BERTopic
        from hdbscan import HDBSCAN
        from sentence_transformers import SentenceTransformer
        from umap import UMAP
    except ImportError as exc:
        raise SystemExit(
            "BERTopic mode requires bertopic, sentence-transformers, "
            "umap-learn, and hdbscan."
        ) from exc

    embedding_model = SentenceTransformer(args.embedding_model)
    embeddings = embedding_model.encode(
        df[text_col].tolist(),
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    umap_model = UMAP(
        n_neighbors=args.umap_neighbors,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=args.random_state,
    )

    hdbscan_model = HDBSCAN(
        min_cluster_size=args.min_cluster_size,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )

    model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        calculate_probabilities=False,
        verbose=True,
    )

    topics, _ = model.fit_transform(df[text_col].tolist(), embeddings)

    info = model.get_topic_info()
    info.to_csv(output_dir / "bertopic_topic_info.csv", index=False)

    assignments = df[[id_col]].copy()
    assignments["bertopic_topic"] = topics
    write_table(assignments, output_dir / "bertopic_document_topics")

    rep_rows = []
    representatives = model.get_representative_docs()
    for topic_id, docs in representatives.items():
        for rank, doc in enumerate(docs, start=1):
            rep_rows.append(
                {
                    "topic": topic_id,
                    "rank": rank,
                    "representative_document": doc,
                }
            )
    write_table(pd.DataFrame(rep_rows), output_dir / "bertopic_representative_docs")

    non_outlier = [t for t in topics if t != -1]
    return {
        "embedding_model": args.embedding_model,
        "n_topics_excluding_outlier": len(set(non_outlier)),
        "outlier_share": float(sum(t == -1 for t in topics) / len(topics)),
        "min_cluster_size": args.min_cluster_size,
        "umap_neighbors": args.umap_neighbors,
        "versions": {
            "bertopic": bertopic.__version__,
            "sentence_transformers": sentence_transformers.__version__,
            "umap": getattr(umap, "__version__", "unknown"),
            "hdbscan": getattr(hdbscan, "__version__", "unknown"),
        },
    }


def main():
    args = parse_args()
    df = read_table(args.input)
    require_columns(df, [args.id_column, args.text_column])

    if df[args.id_column].duplicated().any():
        raise ValueError("ID column must be unique.")

    df = df[[args.id_column, args.text_column]].copy()
    df[args.text_column] = df[args.text_column].fillna("").astype(str)

    output_dir = ensure_output_dir(args.output_dir)
    corpus_meta = df[[args.id_column]].copy()
    corpus_meta["text_sha256"] = df[args.text_column].map(text_sha256)
    write_table(corpus_meta, output_dir / "corpus_metadata")

    manifest = {
        "created_utc": utc_now_iso(),
        "input": str(Path(args.input).resolve()),
        "n_documents": len(df),
        "mode": args.mode,
        "random_state": args.random_state,
        "python": platform.python_version(),
        "research_note": (
            "Topic solutions require stability analysis, random-document review, "
            "domain-expert interpretation, and external/economic validation."
        ),
    }

    if args.mode in {"nmf", "both"}:
        manifest["nmf"] = run_nmf(
            df, args.text_column, args.id_column, args, output_dir
        )

    if args.mode in {"bertopic", "both"}:
        manifest["bertopic"] = run_bertopic(
            df, args.text_column, args.id_column, args, output_dir
        )

    write_json(output_dir / "manifest.json", manifest)
    print(f"Topic-discovery outputs saved to {output_dir}")


if __name__ == "__main__":
    main()
