# Finance & Accounting Methods Advisor

A Codex skill for designing, validating, implementing, and auditing machine-learning, NLP, embedding, LLM, and causal-ML methods in academic finance and accounting research.

## What this skill is for

Use it when the research question is of the form:

- Which computational method should I use?
- Should I use a dictionary, embeddings, BERTopic, BERT, or an LLM?
- How should I validate an LLM-derived research variable?
- How do I turn textual model output into a firm-year measure?
- Is my train/test split leaking firm or temporal information?
- Should I use DoubleML or causal forests?
- How should I write the methods section for this computational measure?
- How should I build an annotation codebook?

This skill is **not** intended primarily for summarizing individual papers. Use a paper-reader skill for that, then use this skill to decide whether and how to adapt the paper's method.

---

# Recommended Folder

```text
finance-accounting-methods-advisor/
├── SKILL.md
├── README.md
├── AGENTS.md
├── references/
│   ├── Finance_Accounting_ML_LLM_Methods_Handbook.md
│   ├── Finance_Accounting_Methods_Advisor_Prompt.md
│   ├── method-selection-matrix.md
│   ├── validation-guidelines.md
│   ├── textual-analysis-and-embeddings.md
│   ├── llm-measurement.md
│   └── causal-ml.md
├── templates/
│   ├── research-design-blueprint.md
│   ├── construct-codebook.md
│   ├── validation-protocol.md
│   ├── methods-section-template.md
│   ├── method-decision-log.md
│   └── reproducibility-checklist.md
├── scripts/
│   ├── scripts-README.md
│   ├── requirements-starter.txt
│   ├── init_research_project.py
│   ├── text_classifier.py
│   ├── embedding_similarity.py
│   ├── topic_discovery.py
│   ├── llm_classification.py
│   ├── doubleml_template.py
│   └── _io_utils.py
└── evals/
    └── evaluation-cases.md
```

---

# Installation

Place the folder in your Codex skills directory.

For example:

```text
C:/Users/<username>/.codex/skills/finance-accounting-methods-advisor/
```

Then restart/reload Codex so the skill is rediscovered.

The exact skills directory can differ by Codex setup; use the same location where your existing custom skills are stored.

---

# How the skill should behave

The advisor follows:

```text
construct
→ unit of analysis
→ task type
→ baseline
→ preferred method
→ validation
→ implementation
→ econometric use
```

It should **not** begin by selecting an algorithm.

Examples:

## Topic discovery

Prompt:

```text
I have SEC comment letters from 2005–2025.
I want to know what types of issues the SEC raises.
```

Expected logic:

```text
individual SEC comment as likely unit
→ genuine discovery task
→ LDA/NMF benchmark
→ BERTopic/embedding clustering
→ stability + human interpretation
→ freeze taxonomy
→ supervised production classification
```

It should not simply report the number of BERTopic clusters as the true number of economic topics.

## Known construct

Prompt:

```text
I want to measure whether chairman statements emphasize innovation.
```

Expected logic:

```text
construct already known
→ not primarily a topic-discovery problem
→ dictionary baseline
→ validated classifier / LLM if semantic nuance matters
→ human gold set
→ firm-year aggregation
```

## Causal ML

Prompt:

```text
I want to use causal forest to show that AI adoption improves firm value.
```

Expected logic:

```text
identify treatment/outcome/timing
→ challenge identification
→ causal forest does not solve endogenous adoption
→ establish credible causal design
→ use causal ML only for justified heterogeneity estimation
```

---

# Suggested Daily Usage

You can ask the skill directly:

```text
Design a publication-quality methodology for...
```

```text
Compare BERTopic, LDA, embeddings, and LLM classification for...
```

```text
Audit the following computational method as if you were a skeptical JAR/JAE/RAST reviewer...
```

```text
Create an annotation codebook for...
```

```text
Create a validation protocol for...
```

```text
Turn this finalized measurement pipeline into a methods-section draft...
```

```text
Write Python for the preferred method after defining the validation strategy.
```

---

# Progressive Reference Loading

The skill is designed to avoid loading every document.

Typical routing:

| Question | Main file |
|---|---|
| method choice | `method-selection-matrix.md` |
| validation | `validation-guidelines.md` |
| text / embeddings / topics | `textual-analysis-and-embeddings.md` |
| LLM measurement | `llm-measurement.md` |
| DML / causal forest | `causal-ml.md` |
| broader details | main handbook |

---

# Templates

## Research Design Blueprint

Use when starting a new project.

Produces a structured plan covering:

- construct
- data
- unit
- baseline
- preferred method
- gold labels
- leakage
- validation
- aggregation
- econometrics
- robustness
- tables/figures
- reviewer risks

## Construct Codebook

Use before annotation or LLM coding.

Defines:

- construct
- unit
- inclusion/exclusion
- ambiguity rules
- positive/negative/boundary examples
- multilabel/ordinal rules
- coder procedure
- gold-set governance

## Validation Protocol

Use before large-scale inference.

Defines:

- gold sample
- splits
- metrics
- error analysis
- construct validity
- method robustness
- domain shift
- thresholds
- acceptance criteria

## Method Decision Log

Use throughout a project to record consequential choices, alternatives, evidence,
risks, and planned robustness tests. Superseded decisions remain visible as an
audit trail.

## Reproducibility Checklist

Use before freezing the empirical dataset or circulating the paper. It covers raw
data provenance, annotation, modeling, leakage, variable construction, the software
environment, and repository-level reproducibility.

## Methods Section

Use only after the design is frozen.

The skill should leave unknown results as placeholders rather than fabricate model performance.

---

# Recommended Companion Skill

A complementary `finance-accounting-paper-reader` skill can answer:

> What did this paper do?

This methods advisor then answers:

> Is that method appropriate for my project, and how should I adapt and validate it?

Keep these roles separate.

---

# Quality Standard

The skill should prefer:

> valid, reproducible, interpretable measurement

over:

> the newest model.

A strong answer should help defend:

```text
theory
→ construct
→ data
→ measurement
→ validation
→ research variable
→ empirical design
→ economic inference
```


# Initialize a New Research Project

The bundle includes `scripts/init_research_project.py`.

For the full starter-pipeline command reference and dependency groups, see
`scripts/scripts-README.md` and `scripts/requirements-starter.txt`.

Example:

```bash
python scripts/init_research_project.py \
  --name sec_comment_novelty \
  --output-root D:/Research/Projects \
  --title "SEC Comment Novelty and Future Restatements"
```

It creates:

```text
project/
├── data/
├── code/
├── prompts/
├── configs/
├── outputs/
├── models/
├── docs/
│   ├── research-design-blueprint.md
│   ├── construct-codebook.md
│   ├── validation-protocol.md
│   ├── method-decision-log.md
│   └── reproducibility-checklist.md
└── manuscript/
    └── methods-section-template.md
```

The project scaffold is intentionally conservative: raw data, model artifacts, `.env`, and generated outputs are excluded or separated so you can decide what is safe and appropriate to commit.
