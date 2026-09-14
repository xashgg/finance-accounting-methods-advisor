# Project Guide for Agents

## Purpose

This repository packages the `finance-accounting-methods-advisor` Codex skill.
It combines routing instructions, methodological references, reusable research
templates, starter Python pipelines, and behavior-focused evaluation cases.

## Source-of-truth map

- `SKILL.md` defines activation, routing, guardrails, and response behavior.
- `references/` contains the detailed methodological guidance loaded selectively.
- `templates/` contains reusable research artifacts; preserve bracketed unknowns
  rather than inventing sample sizes, validation results, or model performance.
- `scripts/` contains conservative starter pipelines, not turnkey research designs.
- `evals/evaluation-cases.md` defines expected behavior and regression checks.
- `README.md` is the human-facing installation and usage overview.

## Maintenance rules

- Keep the workflow construct-first: construct, unit, task, baseline, preferred
  method, validation, implementation, and econometric use.
- Preserve the distinction between discovery and production measurement, and
  between prediction and causal identification.
- Treat LLM output as a measurement instrument that requires human validation.
- Require time-, firm-, document-family-, or group-aware splits when the research
  setting makes random row splits vulnerable to leakage.
- Keep `SKILL.md` compact. Put detailed explanations in the relevant reference and
  route to them from the skill.
- When adding or renaming a reference, template, script, or eval, update the file
  maps and routing tables in `SKILL.md`, `README.md`, and the relevant subdirectory
  guide in the same change.
- Do not hard-code current package behavior without checking official documentation.
- Do not add dependencies unless the methodological benefit justifies them; update
  `scripts/requirements-starter.txt` and `scripts/scripts-README.md` together.

## Verification

Run command-interface smoke checks after script changes:

```text
python -B scripts/init_research_project.py --help
python -B scripts/text_classifier.py --help
python -B scripts/embedding_similarity.py --help
python -B scripts/topic_discovery.py --help
python -B scripts/llm_classification.py --help
python -B scripts/doubleml_template.py --help
```

After changing `SKILL.md` or a reference, rerun at least Evals 1, 3, 5, 7, 8,
and 10 from `evals/evaluation-cases.md`. Verify local paths named in Markdown and
scan for stale relative-time language before handing off.
