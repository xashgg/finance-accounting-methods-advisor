---
title: "Finance & Accounting ML/LLM Methods Handbook"
subtitle: "Research Question → Method → Python → Validation → Paper Reporting"
version: "1.0"
date: "2026-09-14"
tags:
  - finance
  - accounting
  - machine-learning
  - LLM
  - textual-analysis
  - research-methods
---

# Finance & Accounting ML/LLM Methods Handbook

## Purpose

This handbook is designed for empirical finance and accounting research in which machine learning (ML), natural language processing (NLP), embeddings, or large language models (LLMs) are used to **measure constructs, discover patterns, classify text, extract structured information, make predictions, or support causal analysis**.

The handbook is not an algorithm catalog. Its decision order is:

> **Research construct → unit of analysis → task type → baseline method → modern method → validation → reproducibility → econometric use**

The central rule is:

> **Do not select an algorithm because it is fashionable. Select a method because its statistical and measurement properties match the research task.**

---

# 1. The Method-Selection Protocol

Whenever you have a new research question, answer these questions in order.

## 1.1 Define the construct

Write one sentence:

> I want to measure / discover / predict **X** from **Y data** at the **Z unit of analysis**.

Examples:

- I want to measure management uncertainty from earnings-call answers at the response level.
- I want to discover recurring SEC review issues from individual SEC comments.
- I want to measure semantic novelty in annual-report risk factors at the firm-year level.
- I want to predict material misstatements from financial and textual variables at the firm-year level.

If the construct cannot be defined clearly, do not start modeling.

## 1.2 Define the unit of analysis

Typical units:

- document
- filing
- filing section
- paragraph
- sentence
- analyst question
- management answer
- SEC comment
- patent
- news article
- firm-year
- firm-quarter
- event

The unit determines what the model is actually learning.

**Example:** An SEC comment letter may contain several unrelated accounting issues. If the research question concerns regulatory issues, the individual SEC comment is usually a more defensible unit than the complete letter.

## 1.3 Identify the task family

| Research goal | Task family |
|---|---|
| Count a known concept | Dictionary / rule-based measurement |
| Measure lexical similarity | TF-IDF / cosine similarity |
| Measure semantic similarity | Embeddings |
| Discover unknown themes | Topic modeling / clustering |
| Assign known categories | Classification |
| Extract entities, dates, amounts, events | Information extraction / NER / LLM structured extraction |
| Predict an outcome | Supervised ML |
| Detect unusual observations | Anomaly detection |
| Estimate heterogeneous causal effects | Causal ML |
| Convert nuanced language into a construct | LLM-assisted measurement |
| Search a very large text corpus by meaning | Embedding retrieval / reranking |

## 1.4 Always define a baseline

A modern model should usually be compared with a simpler benchmark.

Examples:

| Modern method | Useful baseline |
|---|---|
| BERTopic | LDA / NMF |
| Sentence embeddings | TF-IDF cosine similarity |
| BERT/DeBERTa classifier | logistic regression + TF-IDF |
| LLM classification | dictionary / supervised classifier / human coding |
| XGBoost | OLS/logit / LASSO |
| Causal forest | conventional treatment-effect model |

The baseline helps determine whether sophistication produces genuine measurement or predictive gains.

## 1.5 Design validation before full-sample estimation

Before scaling to millions of documents, decide:

- What is the human-coded validation sample?
- What is the benchmark?
- Which metrics are appropriate?
- What sensitivity tests will be run?
- What model/prompt/version information must be saved?
- What evidence would falsify the proposed measure?

---

# 2. Quick Decision Matrix

| Research question | Preferred starting method | Modern extension | Main validation |
|---|---|---|---|
| Does a disclosure mention a known concept? | Dictionary / regex | LLM classifier | Human-coded precision/recall |
| What is the tone of a filing? | Loughran-McDonald dictionary | FinBERT / LLM | Human labels + convergent validity |
| How similar are two disclosures lexically? | TF-IDF cosine | — | Robustness to preprocessing |
| How similar are two disclosures semantically? | Sentence embeddings | domain-specific embedding model | Human pairwise judgments |
| What topics exist in a corpus? | LDA / NMF | BERTopic / embedding clustering | Stability + human interpretation |
| I know the categories; classify documents | TF-IDF + logit/SVM | BERT/DeBERTa | Held-out precision/recall/F1 |
| I know categories but have few/no labels | Human-coded seed set | LLM zero/few-shot | Human gold set + prompt/model robustness |
| Extract structured facts from text | Regex / NER | LLM structured output | Exact match / field-level accuracy |
| Predict fraud/distress/default | Logit / LASSO | RF / XGBoost / NN | Strict out-of-sample performance |
| Measure novelty | TF-IDF distance | Embedding distance | Human novelty judgments + temporal design |
| Discover anomalous disclosures | Distance/outlier methods | embedding anomaly detection | Case inspection + known events |
| Estimate heterogeneous treatment effects | Interactions / subgroup models | causal forest / DML | Identification + overlap + robustness |
| Search millions of passages | BM25 | dense retrieval + reranker | Recall@k / human relevance |

---

# 3. Method Card: Dictionary and Rule-Based Measurement

## Research use

Use when the construct is defined by known words, phrases, formats, or deterministic rules.

Examples:

- AI disclosure
- cybersecurity disclosure
- forward-looking statements
- financial constraints
- risk terminology
- numeric disclosures
- accounting-standard references

## Strengths

- transparent
- inexpensive
- highly reproducible
- easy to audit
- easy to explain to reviewers

## Weaknesses

- context blindness
- negation problems
- polysemy
- domain drift
- cannot reliably capture nuanced constructs

## Python tools

- `re`
- `pandas`
- `spaCy`
- `flashtext`
- `pyahocorasick`

## Validation

Do not report a dictionary measure without inspecting examples.

Recommended:

1. Draw a stratified sample of positive and negative cases.
2. Human-code whether the construct is actually present.
3. Report precision and recall.
4. Test alternative dictionary definitions.
5. Test sensitivity to document length and boilerplate.

## Canonical finance/accounting references

- Loughran, T., & McDonald, B. (2011). *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.* Journal of Finance.
- Anand, V., Bochkay, K., Chychyla, R., & Leone, A. J. (2020). *Using Python for Text Analysis in Accounting Research.*

---

# 4. Method Card: TF-IDF and Lexical Similarity

## Use when

You want similarity based primarily on **shared terminology** rather than deep semantic equivalence.

Typical applications:

- disclosure change
- boilerplate
- copied text
- product-market similarity
- repeated risk factors
- similarity between annual reports

## Core workflow

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=5
)

X = vectorizer.fit_transform(documents)
S = cosine_similarity(X)
```

## Key design choices

- unigram vs bigram
- stop-word policy
- minimum document frequency
- document section
- stemming/lemmatization
- whether the vocabulary is fit on the full corpus or training/reference corpus

## Important leakage issue

If the variable is intended to measure **novelty relative to prior information**, do not use future documents to construct the comparison vocabulary or reference set when doing so would introduce look-ahead information.

---

# 5. Method Card: Embeddings and Semantic Similarity

## Use when

Different wording can express the same meaning.

Examples:

- semantic disclosure similarity
- management–analyst alignment
- innovation disclosure similarity
- semantic novelty
- mapping comments to accounting issues
- matching research concepts to passages

## Concept

A text is transformed into a vector:

\[
text_i \rightarrow \mathbf{e}_i
\]

Semantic similarity can then be estimated with cosine similarity:

\[
sim(i,j)=\frac{\mathbf e_i \cdot \mathbf e_j}
{\|\mathbf e_i\|\|\mathbf e_j\|}
\]

## Python starter

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(
    documents,
    normalize_embeddings=True,
    show_progress_bar=True
)

similarities = embeddings @ embeddings.T
```

## Model-selection questions

Ask:

- Was the model trained for sentence/document similarity?
- Is the text finance-specific?
- Are documents much longer than the model context window?
- Is multilingual support required?
- Is a domain-specific embedding model materially better?
- Do results survive alternative embedding models?

## Validation

For research constructs based on similarity:

1. Create pairs of texts covering low, medium, and high model similarity.
2. Ask independent human coders to score semantic similarity.
3. Correlate human and model rankings.
4. Examine false-positive high-similarity pairs.
5. Repeat with alternative embedding models.

## Recommended documentation

- Sentence Transformers: https://www.sbert.net/
- Clustering guide: https://www.sbert.net/examples/sentence_transformer/applications/clustering/README.html

---

# 6. Method Card: Topic Discovery

## First question

Do you genuinely want **discovery**, or do you already know the categories?

If categories are theoretically known, classification is often preferable to unsupervised topic modeling.

## 6.1 LDA

Good when:

- you need a classical, interpretable benchmark
- word co-occurrence is substantively informative
- documents are reasonably long
- the mixture-of-topics assumption is acceptable

Important issue:

You generally need to choose the number of topics \(K\).

Do not choose \(K\) only because one automatic metric peaks there. Combine:

- coherence
- topic diversity
- stability
- interpretability
- usefulness for the research construct

## 6.2 NMF

Useful with TF-IDF matrices and often produces interpretable components.

Good benchmark when LDA assumptions are not attractive.

## 6.3 BERTopic

Typical default pipeline:

> embeddings → UMAP → HDBSCAN → c-TF-IDF → topic representation

Advantages:

- semantic embeddings
- does not require specifying a fixed \(K\) in the same way as k-means/LDA
- can identify outliers
- modular pipeline
- representative documents aid interpretation

### Minimal code

```python
from bertopic import BERTopic

topic_model = BERTopic(
    calculate_probabilities=False,
    verbose=True
)

topics, probs = topic_model.fit_transform(documents)

topic_info = topic_model.get_topic_info()
representative_docs = topic_model.get_representative_docs()
```

### Critical caution

The number of BERTopic clusters is **not automatically the number of economically meaningful constructs**.

Topic granularity depends on:

- unit of analysis
- embedding model
- UMAP parameters
- HDBSCAN parameters
- minimum cluster size
- document length
- preprocessing
- corpus composition

## Topic-model validation protocol

A publishable topic model should normally include:

### A. Quantitative diagnostics

Consider:

- topic coherence
- topic diversity
- cluster-size distribution
- outlier share
- silhouette/density diagnostics where appropriate

### B. Stability

Refit under:

- different random seeds
- plausible hyperparameters
- alternative embedding models
- alternative time subsamples
- alternative preprocessing

Ask whether the substantive themes persist.

### C. Human validation

For each major topic:

1. inspect top terms
2. inspect representative documents
3. randomly sample assigned documents
4. have domain-informed coders identify the common construct
5. record whether documents actually belong together

### D. External validity

Check whether topic prevalence changes in theoretically expected settings.

Example:

A revenue-recognition topic should plausibly correlate with industries/accounting regimes where revenue-recognition complexity is higher.

---

# 7. Method Card: Clustering Without Topic Modeling

## k-Means

Use if:

- you have embeddings/features
- you can justify or tune the number of clusters
- roughly centroid-shaped groups are plausible

Problem:

You must specify \(K\).

## Agglomerative clustering

Useful when:

- the number of groups is not known
- hierarchical structure is substantively useful
- data size is manageable

## HDBSCAN

Useful when:

- cluster number is unknown
- clusters can have irregular shapes
- you want an explicit outlier/noise category

Important:

HDBSCAN's output depends strongly on density parameters. Treat cluster count as a modeling outcome, not a scientific fact.

---

# 8. Method Card: Supervised Text Classification

## Use when

You have predefined categories such as:

- revenue recognition
- goodwill impairment
- internal control
- tax
- segment reporting
- non-GAAP
- cybersecurity

and want to assign them to new documents/comments.

## Baseline

Start with:

> TF-IDF + logistic regression or linear SVM

## Modern method

Fine-tune a pretrained Transformer:

- BERT
- RoBERTa
- DeBERTa
- finance-domain model where appropriate

## Data split

At minimum:

- training set
- validation set
- held-out test set

But in finance/accounting, random splitting can be misleading.

Consider grouping or temporal splitting by:

- firm
- year
- filing
- industry
- source document

to avoid near-duplicate leakage.

## Metrics

For binary/multiclass classification:

- precision
- recall
- F1
- macro-F1
- confusion matrix
- PR-AUC for imbalanced problems
- ROC-AUC where appropriate

Do not rely on accuracy alone.

## Hugging Face starting point

https://huggingface.co/docs/transformers/main/tasks/sequence_classification

---

# 9. Method Card: LLM Classification

## Use when

- categories can be defined clearly in natural language
- labeled data are limited
- semantic interpretation is central
- classification is difficult to represent with keyword rules

## Preferred research workflow

Do not begin with:

> “Classify this text into one of these categories.”

Begin with a coding protocol.

Example:

```text
Construct: Revenue-recognition concern

Code 1 if the regulator explicitly questions:
- timing of revenue recognition,
- performance obligations,
- contract consideration,
- principal-vs-agent treatment,
- collectability,
- disaggregation tied to recognition,

and the concern materially relates to recognized or reported revenue.

Code 0 for:
- purely descriptive revenue references,
- segment sales without recognition concerns,
- general growth discussion,
- unrelated receivables issues.
```

Then ask the LLM to apply the coding protocol.

## Structured output

Prefer machine-readable output:

```json
{
  "label": 1,
  "category": "revenue_recognition",
  "evidence": "...",
  "confidence": 0.86
}
```

For the final research dataset, store model output separately from raw source text.

## Validation

A strong validation design includes:

- blinded human gold labels
- inter-rater agreement among humans
- model-human agreement
- precision / recall / F1
- error taxonomy
- alternative prompts
- alternative models
- repeated calls where stochasticity matters
- model/version/date logging

## Key accounting reference

Ties de Kok (2025), *ChatGPT for Textual Analysis? How to Use Generative LLMs in Accounting Research*, Management Science.

The key methodological message is that LLM power does not eliminate the need for construct validation.

---

# 10. Method Card: Information Extraction

## Use when

The target is structured information rather than a conceptual label.

Examples:

- amounts
- dates
- product names
- auditors
- accounting standards
- litigation outcomes
- covenant terms
- disclosed AI systems
- entities and relationships

## Preferred hierarchy

1. regex for deterministic formats
2. dictionary/gazetteer where entities are known
3. NER / supervised extraction
4. LLM structured extraction for complex context

## LLM extraction example

Input:

> Please return only valid JSON conforming to the schema.

Schema:

```json
{
  "issue": "string",
  "accounting_standard": "string|null",
  "amount_usd": "number|null",
  "period": "string|null"
}
```

## Validation

Evaluate each field separately.

Do not report only document-level “accuracy.”

---

# 11. Method Card: Predictive Machine Learning

## Use when

The primary objective is prediction, ranking, or forecasting.

Examples:

- bankruptcy
- fraud
- restatement
- credit risk
- earnings surprise
- analyst forecast errors

## Baselines

- OLS
- logit/probit
- LASSO / elastic net

## Common extensions

- random forest
- gradient boosting
- XGBoost / LightGBM
- neural networks

## Essential distinction

Predictive importance is not causal importance.

A variable that improves out-of-sample prediction does not automatically identify an economically causal mechanism.

## Evaluation

Use true out-of-sample evaluation.

Prefer temporal evaluation when deployment/prediction is temporal.

Potential metrics:

Regression:
- MAE
- RMSE
- out-of-sample \(R^2\)

Classification:
- ROC-AUC
- PR-AUC
- precision
- recall
- F1
- calibration

---

# 12. Method Card: Causal ML

## Use when

The research question concerns treatment effects and flexible nuisance functions or heterogeneous treatment effects.

Examples:

- Which firms benefit most from AI adoption?
- Does a regulation affect certain firms more strongly?
- Are disclosure effects heterogeneous by information environment?

## Core methods

- Double / Debiased Machine Learning
- causal forests
- generalized random forests
- heterogeneous treatment effects
- orthogonalization / cross-fitting

## Critical rule

ML does not solve identification.

You still need:

- defensible treatment definition
- identification assumptions
- timing
- overlap/common support
- no inappropriate post-treatment controls
- credible design

## Python starting point

DoubleML: https://docs.doubleml.org/

---

# 13. Long Documents and Chunking

Financial documents can exceed model context windows and often contain multiple constructs.

Possible units:

- fixed token windows
- sentence groups
- paragraphs
- semantic chunks
- document sections

Prefer economically meaningful boundaries when available.

Examples:

- MD&A section
- Risk Factors section
- individual analyst question/answer
- individual SEC comment
- individual audit matter

## Chunking validation

Check:

- whether chunks break a relevant argument across boundaries
- whether a chunk contains multiple topics
- whether results depend on chunk size
- whether aggregation back to firm-year is defensible

---

# 14. Aggregating Text Measures to Econometric Variables

A text model often operates below the econometric unit.

Example:

\[
comment \rightarrow classification
\]

but regression unit is:

\[
firm-year
\]

Possible aggregations:

- indicator: any comment of type X
- count
- proportion
- maximum severity
- mean score
- weighted score
- number of distinct issues
- entropy/diversity of issues

Each aggregation implies a different construct.

Do not mechanically average scores.

---

# 15. SEC Comment Letter Case Study

## Research question

> How many substantively distinct regulatory issues appear in SEC comment letters, and how does the composition of issues vary across firms and time?

## Step 1: Define observation unit

Prefer individual SEC comments rather than complete letters if letters contain multiple issues.

## Step 2: Build corpus

Store:

- firm identifier / CIK
- letter date
- correspondence ID
- comment number
- comment text
- filing/form referenced
- fiscal year
- industry
- metadata needed for later aggregation

## Step 3: Clean cautiously

Remove:

- headers/footers
- mechanical salutations
- repeated legal boilerplate

Usually preserve:

- accounting terminology
- numbers when economically meaningful
- negation
- standard references

## Step 4: Sample and manually inspect

Before modeling, read a few hundred comments.

Create a preliminary issue taxonomy.

This determines whether the task is truly discovery, classification, or both.

## Step 5: Classical discovery benchmark

Run LDA or NMF across plausible topic counts.

Record:

- coherence
- diversity
- top terms
- representative comments
- human interpretability

## Step 6: Modern discovery

Run BERTopic.

A defensible design compares:

- at least two embedding models
- plausible minimum cluster sizes
- alternative UMAP/HDBSCAN settings
- stability across time subsamples

## Step 7: Human interpretation

For each major topic:

- top terms
- representative comments
- random assigned comments

Have coders provide:

- topic label
- coherence rating
- overlap with adjacent topics
- whether topic should be merged/split

## Step 8: Build stable taxonomy

Example taxonomy might include:

- Revenue recognition
- Segment reporting
- Goodwill / impairment
- Fair value
- Tax
- Internal controls
- Non-GAAP
- Liquidity / going concern
- M&A
- Related-party transactions
- Cybersecurity
- Other disclosure compliance

Do not adopt this list without corpus evidence; it is illustrative.

## Step 9: Convert discovery into measurement

Once the taxonomy is stable, move to supervised classification.

Create a labeled gold sample.

Compare:

1. TF-IDF + logit/SVM
2. BERT/DeBERTa classifier
3. LLM few-shot classifier

Then select the production classifier based on:

- held-out performance
- robustness
- cost
- interpretability
- reproducibility

## Step 10: Aggregate

Construct firm-year variables:

- number of issue categories
- issue-specific indicators
- total comments
- regulatory issue diversity
- novel vs recurring issues
- severity proxies

## Step 11: Validate economically

Examples:

- revenue-recognition concerns and revenue complexity
- goodwill comments and acquisition intensity
- non-GAAP comments and non-GAAP reporting
- internal-control comments and material weaknesses

## Step 12: Paper reporting

Report:

- corpus construction
- unit of analysis
- preprocessing
- model/version
- hyperparameters
- training/test split
- human coding procedure
- validation metrics
- error analysis
- sensitivity tests
- aggregation procedure

---

# 16. Human Annotation Protocol

For model-based measurement, build a gold set.

## Recommended workflow

1. Draft construct definition.
2. Draft inclusion/exclusion rules.
3. Independently code a pilot sample.
4. Discuss disagreements.
5. Revise codebook.
6. Code validation sample independently.
7. Report agreement.
8. Freeze the codebook before model evaluation.

Possible agreement metrics:

- percent agreement
- Cohen's kappa
- Krippendorff's alpha

For ambiguous constructs, preserving disagreement can be informative.

---

# 17. Error Analysis

After model evaluation, do not stop at F1.

Create error categories.

Example:

| Error | Meaning |
|---|---|
| lexical confusion | keywords appear but construct absent |
| implicit context | construct present without obvious keywords |
| multi-label overlap | text contains several issues |
| insufficient context | chunk is too short |
| negation | model reverses meaning |
| accounting-specific meaning | general-language model misinterprets term |
| temporal/domain shift | later-period language differs |
| boilerplate contamination | standardized wording drives result |

Error analysis often tells you how to improve the research design.

---

# 18. Temporal and Firm-Level Leakage

This is a major issue in finance/accounting ML.

Random train/test splitting may put:

- the same firm
- nearly identical boilerplate
- adjacent-year filings
- repeated templates

in both training and test sets.

The model can then appear much stronger than it really is.

Consider:

- group split by firm
- temporal split
- leave-industry-out robustness
- deduplication / near-duplicate checks

Choose the split that best represents the intended inference or deployment setting.

---

# 19. Reproducibility Checklist

Save:

- raw-data acquisition date
- source URLs / identifiers
- source document hashes if feasible
- Python version
- package lockfile
- random seeds
- train/validation/test split IDs
- model name
- model revision/version
- prompts
- system instructions
- generation parameters
- human codebook
- validation labels
- preprocessing code
- aggregation code
- excluded observations and reasons

For API-based LLMs also save:

- API model identifier
- request date
- response schema
- temperature/top-p where configurable
- retry logic
- failed-call log

---

# 20. What to Report in a Finance/Accounting Paper

## Data

- corpus source
- sample period
- unit of text
- exclusions
- document counts
- firm counts
- descriptive statistics

## Construct

- theoretical definition
- why text is informative about it
- why the chosen unit is appropriate

## Method

- baseline
- preferred model
- feature representation
- hyperparameters
- training process
- data split

## Validation

- human coding
- agreement
- held-out metrics
- error analysis
- alternative models
- sensitivity tests

## Variable construction

- document-level score
- aggregation
- scaling/transformation
- missing values
- outliers

## Reproducibility

- software
- model version
- code/data availability
- prompt/codebook appendix

---

# 21. Reviewer-Resistance Checklist

Before submission, ask:

- Why is this computational method necessary?
- What does it measure that a simpler approach cannot?
- Is the construct theoretically defined before modeling?
- Is the unit of analysis justified?
- Is there a simple baseline?
- Is there a human gold standard?
- Could leakage inflate performance?
- Are model choices researcher degrees of freedom?
- Are results robust to plausible alternative models?
- Does the method work equally across time/industries?
- Are outliers/noise handled transparently?
- Is the output converted into an economically interpretable variable?
- Would another researcher be able to reproduce the measure?

---

# 22. GenAI Research-Methods Advisor Protocol

A GenAI advisor using this handbook should NOT immediately write code.

It should follow this order:

## Stage A — Parse the research problem

Return:

1. research construct
2. source data
3. unit of analysis
4. task type
5. prediction vs measurement vs causal objective
6. key ambiguity

## Stage B — Recommend methods

Return:

- simplest defensible baseline
- preferred method
- one serious alternative
- methods that should **not** be used and why

## Stage C — Design validation

Specify:

- human coding
- sample size logic
- evaluation metrics
- robustness checks
- leakage risks
- construct-validity tests

## Stage D — Implementation

Only then provide:

- Python packages
- data structure
- pseudocode
- reproducible starter code

## Stage E — Paper reporting

Provide:

- method description
- tables/figures to report
- appendix items
- likely reviewer objections

---

# 23. Standard Output Template for the Advisor

When asked a methodological question, respond in this structure:

```text
Research objective
------------------
...

Recommended unit of analysis
----------------------------
...

Task type
---------
...

Recommended design
------------------
Baseline:
Preferred:
Alternative:

Why
---
...

Validation plan
---------------
...

Python stack
------------
...

Implementation outline
----------------------
...

Robustness checks
-----------------

What to report in the paper
---------------------------

Likely reviewer concerns
------------------------

Core references
---------------
```

---

# 24. Core Reading Shelf

## Machine learning foundation

**James, Witten, Hastie, Tibshirani, Taylor — An Introduction to Statistical Learning with Applications in Python**

Official site:
https://www.statlearning.com/

Use for:

- regression
- classification
- resampling
- regularization
- trees
- SVMs
- deep learning
- unsupervised learning

## Economics / method selection

**Gentzkow, Kelly & Taddy (2019), “Text as Data,” Journal of Economic Literature**

https://www.aeaweb.org/articles?id=10.1257/jel.20181020

Use for:

- conceptualizing text as economic data
- representation
- prediction
- unsupervised text methods
- economic applications

**Imbens (2019), “Machine Learning Methods That Economists Should Know About,” Annual Review of Economics**

https://doi.org/10.1146/annurev-economics-080217-053433

Use for:

- distinguishing ML and econometric goals
- supervised/unsupervised ML
- causal inference connections

## Accounting textual analysis

**Anand, Bochkay, Chychyla & Leone (2020), “Using Python for Text Analysis in Accounting Research”**

https://www.kellogg.northwestern.edu/academics-research/research/detail/2020/using-python-for-text-analysis-in-accounting-research/

Use for:

- Python
- regex
- textual measurement
- similarity
- EDGAR acquisition
- accounting research examples

**Loughran & McDonald (2011), “When Is a Liability Not a Liability?” Journal of Finance**

https://doi.org/10.1111/j.1540-6261.2010.01625.x

Use for:

- domain-specific measurement
- dictionary construction
- why generic language tools can fail in financial text

## LLMs in accounting research

**Ties de Kok (2025), “ChatGPT for Textual Analysis? How to Use Generative LLMs in Accounting Research,” Management Science 71(9):7888–7906**

https://doi.org/10.1287/mnsc.2023.03253

Use for:

- LLM textual analysis
- prompt design
- model selection
- construct validity
- due diligence in accounting research

## Modern NLP documentation

Sentence Transformers:
https://www.sbert.net/

BERTopic:
https://maartengr.github.io/BERTopic/

Hugging Face text classification:
https://huggingface.co/docs/transformers/main/tasks/sequence_classification

scikit-learn:
https://scikit-learn.org/

## Causal ML

DoubleML:
https://docs.doubleml.org/

---

# 25. Data Sources Useful for Finance/Accounting Text Research

## SEC EDGAR

SEC developer resources:
https://www.sec.gov/about/developer-resources

SEC data APIs:
https://www.sec.gov/search-filings/edgar-application-programming-interfaces

SEC full-text/search resources:
https://www.sec.gov/search-filings

Notes:

- `data.sec.gov` provides REST APIs for submissions history and XBRL data.
- public filing archives remain important for document-level textual research.
- build a local cache for large-scale projects.
- respect SEC access policies and identify automated requests appropriately.

Potential corpora:

- 10-K / 10-Q
- 8-K
- proxy statements
- registration statements
- exhibits
- comment-letter correspondence
- XBRL facts

Other common finance/accounting text sources may include:

- earnings-call transcripts
- analyst reports
- news
- patent text
- corporate websites
- ESG reports
- conference-call Q&A
- shareholder letters

Access rights and licensing must be checked separately.

---

# 26. Recommended Python Research Stack

Core:

```text
pandas
numpy
pyarrow
duckdb
scipy
statsmodels
scikit-learn
```

Text:

```text
regex / re
spaCy
nltk
transformers
sentence-transformers
bertopic
hdbscan
umap-learn
```

ML:

```text
scikit-learn
xgboost
lightgbm
```

Causal ML:

```text
doubleml
econml
```

Research engineering:

```text
jupyter
pytest
pydantic
python-dotenv
tqdm
joblib
```

Large textual datasets:

- store processed tables in Parquet
- use DuckDB/Polars where appropriate
- cache model outputs
- separate raw, intermediate, and final datasets

---

# 27. Project Folder Template

```text
project/
├── README.md
├── environment.yml
├── pyproject.toml
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── validation/
│
├── code/
│   ├── 01_collect/
│   ├── 02_parse/
│   ├── 03_clean/
│   ├── 04_label/
│   ├── 05_model/
│   ├── 06_validate/
│   └── 07_construct_variables/
│
├── prompts/
│   ├── system/
│   ├── classification/
│   └── extraction/
│
├── models/
├── outputs/
│   ├── tables/
│   ├── figures/
│   └── diagnostics/
│
├── docs/
│   ├── construct_definition.md
│   ├── codebook.md
│   ├── modeling_decisions.md
│   └── reproducibility.md
│
└── manuscript/
```

---

# 28. Research-Method Decision Log

For every computational measure, maintain:

```text
Construct:
Unit of analysis:
Data source:
Task type:

Baseline:
Preferred method:
Alternative considered:

Why preferred:

Hyperparameters chosen:
How chosen:

Gold standard:
Validation metrics:

Leakage risks:
Mitigation:

Robustness tests:

Known limitations:

Final variable construction:

Date frozen:
Code commit:
```

This log can later supply much of the methods appendix.

---

# 29. A Practical Rule for GenAI vs Conventional ML

Use an LLM when the task requires substantial **semantic judgment expressible in natural-language coding rules**.

Use conventional ML when:

- you have a large labeled dataset,
- stable low-cost prediction is important,
- repeatability is crucial,
- the task is well represented by a supervised learner.

Use simple rules when:

- the construct is deterministic or nearly deterministic.

Use unsupervised methods when:

- the purpose is genuine discovery rather than measurement of a predefined construct.

A strong research workflow often combines them:

> **unsupervised discovery → human taxonomy → LLM/BERT classification → validation → econometric variable**

---

# 30. Final Principle

For finance/accounting research, the strongest computational contribution is usually not:

> “We used a more advanced model.”

It is:

> **“We developed a theoretically meaningful construct, measured it transparently with an appropriate computational method, validated it against credible benchmarks, showed that the result is robust, and used the resulting measure to answer an economically important question.”**
