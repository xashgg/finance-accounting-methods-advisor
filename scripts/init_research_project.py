"""
Initialize a reproducible finance/accounting computational-research project.

The generated project contains documentation and empty data/output directories.
It does not copy restricted data or secrets.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import date
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True, help="Folder/project name.")
    p.add_argument("--output-root", default=".")
    p.add_argument(
        "--title",
        help="Human-readable project title. Defaults to --name.",
    )
    p.add_argument("--force", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    root = Path(args.output_root).resolve() / args.name

    if root.exists():
        if not args.force:
            raise SystemExit(
                f"{root} already exists. Use --force only if you intentionally "
                "want to add missing scaffold files."
            )
    else:
        root.mkdir(parents=True)

    skill_root = Path(__file__).resolve().parent.parent
    template_root = skill_root / "templates"

    dirs = [
        "data/raw",
        "data/interim",
        "data/processed",
        "data/validation",
        "code/01_collect",
        "code/02_parse",
        "code/03_measure",
        "code/04_validate",
        "code/05_construct_variables",
        "code/06_analysis",
        "prompts",
        "configs",
        "outputs/tables",
        "outputs/figures",
        "outputs/diagnostics",
        "models",
        "docs",
        "manuscript",
    ]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)

    template_map = {
        "research-design-blueprint.md": "docs/research-design-blueprint.md",
        "construct-codebook.md": "docs/construct-codebook.md",
        "validation-protocol.md": "docs/validation-protocol.md",
        "method-decision-log.md": "docs/method-decision-log.md",
        "reproducibility-checklist.md": "docs/reproducibility-checklist.md",
        "methods-section-template.md": "manuscript/methods-section-template.md",
    }

    for src_name, dest_name in template_map.items():
        src = template_root / src_name
        dest = root / dest_name
        if src.exists() and not dest.exists():
            shutil.copy2(src, dest)

    config = {
        "project_name": args.name,
        "project_title": args.title or args.name,
        "created": date.today().isoformat(),
        "construct": None,
        "modeling_unit": None,
        "final_empirical_unit": None,
        "task_family": None,
        "baseline_method": None,
        "preferred_method": None,
        "split_strategy": None,
        "primary_validation_metric": None,
        "random_seed": 42,
    }
    config_path = root / "configs" / "project_config.json"
    if not config_path.exists():
        config_path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    gitignore = """\
.env
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
data/raw/*
!data/raw/.gitkeep
models/*
!models/.gitkeep
outputs/*
!outputs/.gitkeep
"""
    gi = root / ".gitignore"
    if not gi.exists():
        gi.write_text(gitignore, encoding="utf-8")

    for placeholder in [
        "data/raw/.gitkeep",
        "models/.gitkeep",
        "outputs/.gitkeep",
    ]:
        (root / placeholder).touch(exist_ok=True)

    readme = f"""# {args.title or args.name}

Computational finance/accounting research project initialized with the
Finance & Accounting Methods Advisor scaffold.

## Start here

1. Complete `docs/research-design-blueprint.md`.
2. If human/LLM coding is needed, complete `docs/construct-codebook.md`.
3. Freeze `docs/validation-protocol.md` before full-corpus inference.
4. Record consequential choices in `docs/method-decision-log.md`.
5. Update `configs/project_config.json`.
6. Keep raw data immutable and outside Git when restricted.
7. Complete `docs/reproducibility-checklist.md` before final circulation.

## Research workflow

```text
construct
→ data/unit
→ baseline
→ preferred method
→ validation
→ full inference
→ aggregation
→ econometrics
→ robustness
```
"""
    project_readme = root / "README.md"
    if not project_readme.exists():
        project_readme.write_text(readme, encoding="utf-8")

    print(f"Initialized project at: {root}")


if __name__ == "__main__":
    main()
