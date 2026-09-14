# Method Selection Matrix
## Finance & Accounting Methods Advisor

Use this file when the main question is:

> **What computational method should I use for this research problem?**

Do not choose a method by novelty. Route from the **research objective and construct**.

---

# 1. First classify the task

| If the researcher wants to... | Task family | Default starting point |
|---|---|---|
| detect a known word, phrase, standard, or explicit disclosure | rule-based measurement | regex / dictionary |
| measure tone using known lexical categories | dictionary measurement | domain dictionary |
| compare wording or textual reuse | lexical similarity | TF-IDF + cosine |
| compare meaning despite different wording | semantic similarity | embeddings |
| find previously unknown themes | unsupervised discovery | LDA/NMF + BERTopic/embedding clustering |
| assign known categories to text | classification | TF-IDF + linear classifier baseline |
| classify with little/no labeled data | weak/zero-shot classification | LLM or zero-shot model + human gold set |
| extract facts, names, dates, amounts, relations | information extraction | regex/NER; LLM for complex context |
| predict a future/observed outcome | supervised prediction | OLS/logit/LASSO + ML alternative |
| identify unusual language or observations | anomaly detection | distance/outlier methods |
| retrieve passages by meaning | information retrieval | BM25 baseline + dense embeddings |
| estimate heterogeneous causal effects | causal ML | conventional identification first, then DML/causal forest if justified |

---

# 2. Decision tree

## A. Is the construct already known?

### Yes

Ask whether the construct can be captured by deterministic rules.

- If **yes** → use regex/dictionary first.
- If **no**, but categories are clearly defined → use classification.
- If classification labels are scarce → consider LLM zero/few-shot with a human gold sample.
- If labels are plentiful → prefer supervised ML/Transformer with held-out validation.

### No

The task is discovery.

Use:

1. qualitative corpus inspection;
2. LDA/NMF as a classical benchmark where appropriate;
3. embedding clustering / BERTopic for semantic discovery;
4. human interpretation and stability testing;
5. freeze a taxonomy;
6. move to supervised measurement if the taxonomy becomes stable.

---

# 3. Dictionary / Regex

## Choose when

- the target is explicit and lexical;
- false positives can be controlled with transparent rules;
- reproducibility matters more than nuanced semantic judgment.

## Good finance/accounting examples

- mentions of AI
- ASC/IFRS standard references
- cybersecurity terminology
- disclosure of specific accounting methods
- numerical pattern extraction
- forward-looking statement markers

## Avoid when

- meaning depends heavily on context;
- negation reverses meaning;
- the same term has multiple domain meanings;
- the construct is implicit rather than explicit.

## Baseline role

Even when using LLMs or Transformers, a dictionary can provide a transparent benchmark.

---

# 4. TF-IDF + Cosine Similarity

## Choose when

The research construct is fundamentally about:

- textual reuse;
- copied language;
- disclosure change;
- lexical novelty;
- wording similarity.

## Prefer embeddings instead when

Two texts can express the same concept with very different vocabulary.

## Validation

- inspect low/medium/high similarity pairs;
- test preprocessing choices;
- test n-grams and vocabulary thresholds;
- avoid future-information leakage in the comparison/reference corpus.

---

# 5. Sentence Embeddings

## Choose when

The construct is semantic rather than lexical.

Examples:

- semantic novelty
- management–analyst alignment
- similarity between disclosures and a concept definition
- matching SEC comments to accounting issues
- semantic search

## Key decisions

- text unit
- embedding model
- domain specificity
- context-window handling
- cosine vs another metric
- temporal reference set
- aggregation to firm-year

## Prefer supervised classification instead when

The researcher already has a stable taxonomy and enough labeled data.

---

# 6. LDA / NMF

## Choose when

- genuine topic discovery is the objective;
- an interpretable classical benchmark is valuable;
- bag-of-words structure is acceptable.

## LDA is attractive when

- documents are not extremely short;
- mixed-topic documents are plausible;
- the researcher can justify or evaluate candidate topic counts.

## NMF is attractive when

- TF-IDF representation is useful;
- sparse linear components yield interpretable themes.

## Do not use merely because

"topic modeling" appears in prior papers.

The unit of analysis and corpus structure must support the method.

---

# 7. BERTopic / Embedding Clustering

## Choose when

- semantic topic discovery is needed;
- documents may be short;
- conventional word co-occurrence misses semantic similarity;
- unknown cluster count is part of the problem.

## Important

BERTopic does **not** reveal an objectively true topic count.

Results depend on:

- embedding model
- UMAP
- HDBSCAN
- minimum cluster size
- preprocessing
- document segmentation
- corpus composition

## Required benchmark

Usually compare against LDA or NMF unless there is a strong reason not to.

## Required validation

- parameter sensitivity
- stability
- representative documents
- random cluster members
- human/domain-expert labeling
- external/economic validity

---

# 8. Classical Supervised Text Classification

## Baseline

Use:

- TF-IDF + logistic regression
- TF-IDF + linear SVM

These are strong, transparent baselines.

## Choose when

- categories are already defined;
- a labeled sample exists;
- interpretability and efficiency matter.

## Advantages

- cheap
- reproducible
- easy to diagnose
- often surprisingly competitive

## Move beyond it when

semantic nuance materially limits the baseline.

---

# 9. BERT / RoBERTa / DeBERTa / Domain Transformers

## Choose when

- categories are known;
- labeled examples exist;
- semantic context matters;
- classical sparse models underperform.

## Requirements

- careful train/validation/test split
- leakage controls
- class-level metrics
- error analysis
- domain-shift checks

## Finance/accounting caution

Random splits can overstate performance because adjacent firm-years, repeated boilerplate, and similar filing templates can appear in both train and test.

---

# 10. LLM Classification

## Choose when

- categories can be described clearly in natural language;
- semantic judgment is central;
- labeled data are limited;
- rapid prototyping or annotation assistance is useful.

## Strong use cases

- nuanced disclosure coding
- managerial evasiveness
- strategic framing
- categorizing complex SEC comments
- classifying reasoning or intent

## Avoid when

- deterministic rules suffice;
- cost at scale is prohibitive;
- reproducibility cannot be managed;
- no credible human validation is possible.

## Required design

- construct definition
- inclusion/exclusion rules
- structured output
- human gold sample
- held-out evaluation
- prompt/model robustness
- version logging

---

# 11. LLM Structured Extraction

## Choose when

The task is to extract structured facts from semantically complex text.

Examples:

- accounting issue
- referenced standard
- disclosed amount
- affected period
- counterparties
- reasons for a management decision

## Prefer regex/NER when

The target follows stable deterministic patterns.

## Evaluate

At the field level, not only at the document level.

---

# 12. Predictive ML

## Baseline

- OLS for continuous outcomes
- logit/probit for binary outcomes
- LASSO / elastic net for high-dimensional linear prediction

## Alternatives

- random forest
- XGBoost / LightGBM
- neural networks

## Choose when

The research objective is genuinely predictive.

## Do not infer

- causality from SHAP values;
- mechanisms from feature importance;
- structural interpretation from predictive rankings.

---

# 13. Causal ML

## Consider only when

A credible causal design already exists.

Potential goals:

- flexible nuisance estimation;
- heterogeneous treatment effects;
- high-dimensional confounding under defensible assumptions.

## Candidate methods

- Double/Debiased ML
- causal forests
- generalized random forests
- EconML estimators

## Do not use causal ML to repair

- endogenous treatment;
- bad timing;
- post-treatment controls;
- weak instruments;
- absent overlap;
- fundamentally non-credible identification.

---

# 14. Retrieval

## Sparse baseline

- BM25 / lexical search

## Dense retrieval

- sentence/document embeddings
- vector database

## Reranking

Use cross-encoders or LLM reranking when higher precision at top-k matters.

## Research uses

- locate passages relevant to a construct;
- retrieve comparable disclosure language;
- assist manual coding;
- build candidate sets before expensive LLM analysis.

## Validation

- Recall@k
- Precision@k
- human relevance judgments

---

# 15. Anomaly / Novelty Detection

## Choose when

The construct is unusualness rather than category membership.

Possible approaches:

- distance from historical centroid
- nearest-neighbor distance
- embedding distance
- Isolation Forest
- Local Outlier Factor

## Finance/accounting caution

Novelty often requires a **time-respecting reference set**.

For observation at time \(t\), compare only with information available before or at \(t\), depending on the construct definition.

---

# 16. Common method-selection mistakes

Avoid these patterns:

### Mistake 1
> "I have text, therefore I should use an LLM."

Correction: determine whether deterministic rules, sparse models, or embeddings solve the construct more transparently.

### Mistake 2
> "BERTopic found 37 clusters, therefore there are 37 topics."

Correction: cluster count is model- and parameter-dependent.

### Mistake 3
> "BERT accuracy is 95%, so the measure is valid."

Correction: check leakage, class imbalance, domain shift, gold-label quality, and economic construct validity.

### Mistake 4
> "XGBoost says variable X is important, therefore X causes Y."

Correction: prediction is not identification.

### Mistake 5
> "An LLM can code everything, so human coding is unnecessary."

Correction: human coding is usually the validation anchor for novel constructs.

---

# 17. Default comparison set

When in doubt, compare methods in tiers.

## Text measurement

**Tier 1 — Transparent baseline**
- regex / dictionary / TF-IDF

**Tier 2 — Conventional ML**
- logit / SVM / LASSO

**Tier 3 — Modern NLP**
- embeddings / Transformer

**Tier 4 — Generative LLM**
- zero/few-shot classification
- structured extraction

The preferred method is the least complex method that achieves acceptable validity for the research construct.

---

# 18. Minimal recommendation template

When this file is loaded, structure the recommendation as:

```text
Research construct:
Unit of analysis:
Task family:

Baseline:
Preferred method:
Alternative:

Why preferred:
Why not the other methods:

Validation:
Leakage/design risks:
What to report:
```

---

# 19. Escalation rule

If method selection remains ambiguous after applying this matrix:

1. inspect a representative sample of the raw data;
2. define the construct more precisely;
3. create a small human-labeled pilot set;
4. benchmark two or three candidate methods;
5. choose based on validity and stability, not sophistication.
