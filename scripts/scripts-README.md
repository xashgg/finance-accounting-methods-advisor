# Starter Python Pipelines

These scripts are **research scaffolds**, not substitutes for research design.

Use them only after the Methods Advisor has established:

1. construct;
2. unit of analysis;
3. task type;
4. baseline;
5. validation plan;
6. leakage/timing rules.

They intentionally avoid several dangerous defaults:

- `text_classifier.py` requires an explicit train/validation/test split column rather than silently creating a random split.
- `llm_classification.py` requires a coding-protocol file and structured output.
- `embedding_similarity.py` records model/provenance metadata.
- `topic_discovery.py` writes both topic diagnostics and document assignments; topic counts remain modeling outcomes, not "truth."
- `doubleml_template.py` supports externally defined group-aware cross-fitting and warns that DML does not create causal identification.

## Files

```text
scripts/
├── _io_utils.py
├── init_research_project.py
├── embedding_similarity.py
├── topic_discovery.py
├── text_classifier.py
├── llm_classification.py
├── doubleml_template.py
└── requirements-starter.txt
```

Install the complete starter dependency set with:

```bash
pip install -r scripts/requirements-starter.txt
```

## Initialize a research project

```bash
python scripts/init_research_project.py \
  --name sec_comment_novelty \
  --output-root D:/Research/Projects \
  --title "SEC Comment Novelty and Future Restatements"
```

The initializer copies the six templates into `docs/` and `manuscript/`, creates
the data, code, prompt, configuration, model, and output directories, and writes
a conservative `.gitignore`. It refuses to overwrite an existing project unless
`--force` is supplied; even then, it adds only missing scaffold files.

## Typical dependencies

Core:

```bash
pip install pandas pyarrow numpy scikit-learn joblib
```

Embeddings:

```bash
pip install sentence-transformers
```

BERTopic:

```bash
pip install bertopic umap-learn hdbscan
```

LLM coding with OpenAI:

```bash
pip install openai pydantic
```

DoubleML:

```bash
pip install doubleml
```

Use a project-specific locked environment for actual research.

## Data format

The scripts accept `.csv` or `.parquet` tables.

Always preserve stable identifiers such as:

```text
document_id
firm_id
date
paragraph_id
```

Never rely on row order as the only identifier.

## Example: baseline text classifier

```bash
python scripts/text_classifier.py \
  --input data/labeled.parquet \
  --id-column comment_id \
  --text-column text \
  --label-column label \
  --split-column split \
  --output-dir outputs/text_classifier
```

The `split` column must contain `train`, `valid`, and `test`.

## Example: embeddings

```bash
python scripts/embedding_similarity.py \
  --input data/comments.parquet \
  --id-column comment_id \
  --text-column text \
  --model sentence-transformers/all-MiniLM-L6-v2 \
  --output-dir outputs/embeddings
```

## Example: topic discovery

```bash
python scripts/topic_discovery.py \
  --input data/comments.parquet \
  --id-column comment_id \
  --text-column text \
  --mode both \
  --nmf-topics 20 \
  --output-dir outputs/topics
```

Do not infer that `20` or the number of BERTopic clusters is the true number of economic topics. Compare solutions and validate them.

## Example: LLM classification

First create a coding protocol file such as:

```text
Construct: Revenue-recognition concern

Positive when...
Negative when...
Ambiguous cases...
```

Then:

```bash
python scripts/llm_classification.py \
  --input data/comments_to_code.parquet \
  --id-column comment_id \
  --text-column text \
  --codebook prompts/revenue_codebook.txt \
  --labels revenue_recognition other \
  --model YOUR_API_MODEL_ID \
  --output outputs/llm_predictions.jsonl
```

The script uses the OpenAI Responses API structured-output interface when installed/configured. Use `--dry-run` to generate request previews without API calls.

## Example: DoubleML

```bash
python scripts/doubleml_template.py \
  --input data/analysis.parquet \
  --outcome roa \
  --treatment ai_adoption \
  --covariates size leverage age cashflow \
  --group-column firm_id \
  --design irm \
  --output-dir outputs/dml
```

`IRM` assumes a binary treatment under an appropriate unconfoundedness design. The script does not make that identification assumption credible for you.

## Output portability

The starter scripts prefer Parquet for tabular outputs. If a Parquet engine is
not installed, they fall back to CSV rather than failing. For real research
projects, install `pyarrow` and use Parquet for large intermediate datasets.
