"""Shared lightweight I/O/provenance utilities for research starter scripts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


def read_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported input format: {suffix}. Use .csv or .parquet.")


def require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def ensure_output_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def write_table(
    df: pd.DataFrame,
    path_without_suffix: str | Path,
    prefer_parquet: bool = True,
) -> Path:
    """Write Parquet when available; fall back to CSV if no Parquet engine exists."""
    base = Path(path_without_suffix)
    base.parent.mkdir(parents=True, exist_ok=True)

    if prefer_parquet:
        parquet_path = base.with_suffix(".parquet")
        try:
            df.to_parquet(parquet_path, index=False)
            return parquet_path
        except ImportError:
            pass

    csv_path = base.with_suffix(".csv")
    df.to_csv(csv_path, index=False)
    return csv_path
