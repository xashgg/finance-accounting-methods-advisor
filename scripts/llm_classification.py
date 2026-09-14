"""
Structured LLM classification starter for research measurement.

The script requires an explicit codebook and writes one JSONL record per source
observation. It supports --dry-run to inspect prompts before making API calls.

The OpenAI implementation follows the Responses API structured-output pattern
(client.responses.parse(..., text_format=PydanticModel)).
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Optional

from _io_utils import read_table, require_columns, text_sha256, utc_now_iso


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--id-column", required=True)
    p.add_argument("--text-column", required=True)
    p.add_argument("--codebook", required=True)
    p.add_argument("--labels", nargs="+", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--prompt-version", default="v1")
    p.add_argument("--max-rows", type=int)
    p.add_argument("--sleep-seconds", type=float, default=0.0)
    p.add_argument("--max-retries", type=int, default=3)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def build_user_prompt(text: str, labels: list[str]) -> str:
    return (
        "Apply the coding protocol to the text below.\n\n"
        f"Allowed labels: {labels}\n\n"
        "Return the single best label under the protocol. "
        "Use a concise evidence field based only on the supplied text.\n\n"
        "TEXT:\n"
        f"{text}"
    )


def main():
    args = parse_args()
    df = read_table(args.input)
    require_columns(df, [args.id_column, args.text_column])

    if df[args.id_column].duplicated().any():
        raise ValueError("ID column must be unique.")

    if args.max_rows:
        df = df.head(args.max_rows).copy()

    codebook = Path(args.codebook).read_text(encoding="utf-8").strip()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        with output_path.open("w", encoding="utf-8") as f:
            for _, row in df.iterrows():
                record = {
                    "id": row[args.id_column],
                    "text_sha256": text_sha256(str(row[args.text_column])),
                    "model": args.model,
                    "prompt_version": args.prompt_version,
                    "system_prompt": codebook,
                    "user_prompt": build_user_prompt(
                        str(row[args.text_column]), args.labels
                    ),
                    "dry_run": True,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"Dry-run requests saved to {output_path}")
        return

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY is not set. Use --dry-run if you only want prompt previews."
        )

    try:
        from openai import OpenAI
        from pydantic import BaseModel, Field
    except ImportError as exc:
        raise SystemExit("Install openai and pydantic.") from exc

    class ClassificationResult(BaseModel):
        label: str
        evidence: Optional[str] = None
        confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)

    client = OpenAI()

    with output_path.open("w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            source_id = row[args.id_column]
            text = str(row[args.text_column])
            user_prompt = build_user_prompt(text, args.labels)

            last_error = None
            parsed = None
            response_id = None

            for attempt in range(1, args.max_retries + 1):
                try:
                    response = client.responses.parse(
                        model=args.model,
                        input=[
                            {"role": "system", "content": codebook},
                            {"role": "user", "content": user_prompt},
                        ],
                        text_format=ClassificationResult,
                    )
                    response_id = getattr(response, "id", None)
                    parsed = response.output_parsed
                    break
                except Exception as exc:  # Preserve failed calls in research log.
                    last_error = repr(exc)
                    if attempt < args.max_retries:
                        time.sleep(min(2 ** (attempt - 1), 8))

            record = {
                "id": source_id,
                "text_sha256": text_sha256(text),
                "created_utc": utc_now_iso(),
                "model": args.model,
                "prompt_version": args.prompt_version,
                "response_id": response_id,
                "label": None,
                "evidence": None,
                "confidence": None,
                "parse_status": "failed",
                "error": last_error,
            }

            if parsed is not None:
                label = parsed.label
                if label not in args.labels:
                    record["parse_status"] = "invalid_label"
                    record["error"] = f"Returned label not in allowed labels: {label}"
                else:
                    record.update(
                        {
                            "label": label,
                            "evidence": parsed.evidence,
                            "confidence": parsed.confidence,
                            "parse_status": "ok",
                            "error": None,
                        }
                    )

            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()

            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)

    print(f"LLM classification records saved to {output_path}")
    print(
        "Research note: self-reported confidence is not calibrated probability. "
        "Evaluate against a held-out human gold set."
    )


if __name__ == "__main__":
    main()
