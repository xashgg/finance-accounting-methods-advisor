"""
Create reproducible sentence embeddings and optional pairwise similarity scores.

Research use:
- semantic similarity
- semantic search preparation
- concept proximity
- novelty pipelines

This script deliberately does NOT compute all-pairs similarity by default because
that is O(n^2) and often inappropriate for large financial-text corpora.
"""

from __future__ import annotations

import argparse
import platform
from pathlib import Path

import numpy as np
import pandas as pd

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
        "--model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence Transformers model name/path.",
    )
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--output-dir", required=True)
    p.add_argument(
        "--pair-file",
        help="Optional CSV/Parquet with columns id_a,id_b for scored pairs.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    try:
        import sentence_transformers
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "Install sentence-transformers before running this script."
        ) from exc

    df = read_table(args.input)
    require_columns(df, [args.id_column, args.text_column])

    if df[args.id_column].duplicated().any():
        raise ValueError("ID column must be unique for embedding provenance.")

    df = df[[args.id_column, args.text_column]].copy()
    df[args.text_column] = df[args.text_column].fillna("").astype(str)

    output_dir = ensure_output_dir(args.output_dir)

    model = SentenceTransformer(args.model)
    embeddings = model.encode(
        df[args.text_column].tolist(),
        batch_size=args.batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    np.save(output_dir / "embeddings.npy", embeddings)

    metadata = pd.DataFrame(
        {
            args.id_column: df[args.id_column].values,
            "embedding_row": np.arange(len(df)),
            "text_sha256": df[args.text_column].map(text_sha256),
            "embedding_model": args.model,
        }
    )
    write_table(metadata, output_dir / "embedding_metadata")

    if args.pair_file:
        pairs = read_table(args.pair_file)
        require_columns(pairs, ["id_a", "id_b"])

        row_map = dict(
            zip(metadata[args.id_column].astype(str), metadata["embedding_row"])
        )

        def get_row(raw_id: object) -> int:
            key = str(raw_id)
            if key not in row_map:
                raise KeyError(f"Pair ID not found in embedded corpus: {key}")
            return int(row_map[key])

        a_idx = np.array([get_row(x) for x in pairs["id_a"]])
        b_idx = np.array([get_row(x) for x in pairs["id_b"]])

        # Because embeddings are normalized, dot product == cosine similarity.
        pairs = pairs.copy()
        pairs["cosine_similarity"] = np.sum(
            embeddings[a_idx] * embeddings[b_idx], axis=1
        )
        write_table(pairs, output_dir / "pair_similarity")

    write_json(
        output_dir / "manifest.json",
        {
            "created_utc": utc_now_iso(),
            "input": str(Path(args.input).resolve()),
            "id_column": args.id_column,
            "text_column": args.text_column,
            "n_rows": len(df),
            "embedding_dim": int(embeddings.shape[1]),
            "model": args.model,
            "normalized_embeddings": True,
            "batch_size": args.batch_size,
            "python": platform.python_version(),
            "sentence_transformers": sentence_transformers.__version__,
            "research_note": (
                "If these embeddings define a research construct, validate semantic "
                "similarity against human-rated text pairs and test an alternative model."
            ),
        },
    )

    print(f"Saved {len(df):,} embeddings to {output_dir}")


if __name__ == "__main__":
    main()
