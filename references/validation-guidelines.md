# Validation Guidelines
## Finance & Accounting Methods Advisor

Use this file when the main question is:

> **How do I demonstrate that an ML/NLP/LLM-based construct or prediction is credible enough for academic research?**

Validation should be designed **before** full-corpus inference.

The core principle is:

> **A model can be statistically accurate yet measure the wrong economic construct.**

---

# 1. Match validation to the research objective

| Objective | Primary validation target |
|---|---|
| dictionary/rule-based measure | precision, recall, rule transparency |
| semantic similarity measure | human pairwise judgments, robustness |
| topic discovery | stability, interpretability, external validity |
| supervised classification | held-out predictive metrics + construct validity |
| LLM classification | human gold set + prompt/model robustness |
| information extraction | field-level exact/partial accuracy |
| prediction | true out-of-sample performance + calibration |
| causal ML | identification assumptions + treatment-effect robustness |
| retrieval | Recall@k / Precision@k + human relevance |

Do not use one generic validation recipe for every method.

---

# 2. Human gold-standard design

For novel finance/accounting constructs, a human-coded gold set is usually the strongest validation anchor.

## Recommended process

1. Define the construct.
2. Write inclusion rules.
3. Write exclusion rules.
4. Include positive and negative examples.
5. Pilot-code a small sample.
6. Discuss disagreements.
7. revise the codebook;
8. freeze the codebook;
9. independently code the validation sample;
10. evaluate the model only after the gold labels are frozen.

## Sampling

Do not draw only easy examples.

Consider stratifying by:

- year
- industry
- firm size
- document type
- model confidence
- predicted class
- rare categories
- text length
- source

For a binary classifier, ensure the validation set contains enough positive cases to estimate recall and precision meaningfully.

## Avoid

Using the same examples to:

- invent the construct,
- tune the prompt,
- choose the model,
- and evaluate final performance.

That produces optimistic validation.

---

# 3. Human agreement

If the construct requires judgment, report agreement among human coders.

Potential statistics:

- percent agreement
- Cohen's kappa
- Krippendorff's alpha

Use the metric appropriate to:

- number of coders
- nominal/ordinal scale
- missing labels

Low human agreement is not merely a labeling problem; it may indicate that the construct is poorly defined.

---

# 4. Classification metrics

## Binary classification

Report at least:

- precision
- recall
- F1
- confusion matrix

Consider:

- PR-AUC for rare events
- ROC-AUC
- specificity
- negative predictive value
- calibration

## Multiclass classification

Report:

- per-class precision
- per-class recall
- per-class F1
- macro-F1
- weighted-F1 where useful
- confusion matrix

Do not let a dominant class hide weak performance on economically important rare classes.

## Multilabel classification

Report:

- per-label metrics
- micro/macro averages
- exact-match ratio only as a supplementary metric

---

# 5. Why accuracy is often insufficient

Example:

If only 5% of SEC comments relate to a rare accounting issue, a classifier that predicts "no" for every case achieves 95% accuracy but has zero research value for identifying the issue.

For imbalanced problems, emphasize:

- recall of the positive class
- precision of the positive class
- F1
- PR-AUC

Choose the operating threshold to match the research use.

---

# 6. Threshold selection

If a model returns probabilities or scores, do not default mechanically to 0.5.

Possible threshold criteria:

- maximize F1
- target minimum precision
- target minimum recall
- minimize a research-specific loss
- choose based on validation-set utility

If the downstream regression is sensitive to false positives versus false negatives, state which error is more costly and why.

Freeze the threshold before evaluating the final test set.

---

# 7. Error analysis

After aggregate metrics, inspect errors manually.

Create an error taxonomy such as:

| Error type | Example implication |
|---|---|
| keyword false positive | dictionary context failure |
| implicit language | model misses nonliteral expression |
| negation | polarity reversal |
| multi-topic text | single-label taxonomy may be wrong |
| insufficient context | unit too short |
| excessive context | unit mixes constructs |
| finance-specific meaning | generic model misreads terminology |
| boilerplate | template language drives prediction |
| temporal shift | new terminology emerges |
| OCR/parsing error | data quality, not model, causes failure |

Use error analysis to revise:

- construct definition
- text unit
- codebook
- preprocessing
- model
- aggregation

Do not merely add model complexity.

---

# 8. Convergent validity

Ask whether the new measure correlates with other measures that should capture a related construct.

Examples:

- an LLM uncertainty score vs a validated uncertainty dictionary;
- semantic novelty vs textual-change measures;
- AI-disclosure classifier vs hand-coded AI adoption events.

A moderate correlation can be desirable if the new measure captures a broader or more semantic construct.

Do not require near-perfect correlation if the new construct is intentionally different.

---

# 9. Discriminant validity

Demonstrate that the measure is not simply capturing a neighboring construct.

Examples:

A "management evasiveness" measure should not merely proxy for:

- answer length
- negative tone
- uncertainty
- readability

A "regulatory severity" measure should not simply proxy for:

- number of comments
- letter length
- firm size

Use:

- correlations
- regression controls
- matched examples
- human review

---

# 10. Economic / external validity

A useful finance/accounting measure should behave plausibly in settings predicted by institutional knowledge or theory.

Examples:

- revenue-recognition concerns should be more common in complex revenue settings;
- goodwill issues may be more prevalent among acquisition-intensive firms;
- internal-control concerns may align with known material weaknesses;
- cybersecurity disclosure may increase after relevant regulatory or incident shocks.

These tests support interpretation but do not replace direct measurement validation.

---

# 11. Topic-model validation

Do not evaluate topic models with a single scalar metric.

Use multiple layers.

## A. Quantitative diagnostics

Possible diagnostics:

- coherence
- topic diversity
- cluster-size distribution
- outlier rate
- silhouette/density metrics where appropriate

Treat these as diagnostics, not proof of substantive validity.

## B. Stability

Refit under:

- alternative random seeds
- nearby hyperparameters
- different embedding models
- alternative preprocessing
- time subsamples
- industry subsamples

Ask:

- do similar substantive topics recur?
- do labels remain stable?
- do major clusters split or merge unpredictably?

## C. Human interpretability

For each topic/cluster inspect:

- top terms
- representative documents
- random assigned documents

Have coders answer:

- Is there one coherent theme?
- Is the label accurate?
- Should the topic split?
- Should it merge with another topic?
- Are many members unrelated?

## D. External validity

Test whether topic prevalence varies in economically expected ways.

---

# 12. Embedding validation

If embeddings are used to define similarity, novelty, or distance:

1. sample text pairs across the score distribution;
2. have humans rate semantic similarity or novelty;
3. compare human rankings with model scores;
4. inspect high-score false positives;
5. inspect low-score false negatives;
6. repeat with alternative embedding models.

If the construct is temporal novelty, validate against a time-respecting reference set.

---

# 13. LLM validation

Treat the prompt as part of the measurement instrument.

## Freeze and save

- system prompt
- user prompt template
- few-shot examples
- output schema
- model ID/version
- date
- temperature/top-p if configurable
- retries
- failure-handling logic

## Test robustness to

- prompt wording
- order of examples
- model family
- model version
- temperature/stochasticity where relevant

## Avoid

Prompt-tuning on the final test labels.

Use:

- development set for prompt design;
- validation set for threshold/model choices;
- held-out test set for final reporting.

---

# 14. Information-extraction validation

Evaluate each field separately.

For example:

```text
issue_type
accounting_standard
amount
currency
period
counterparty
```

Possible metrics:

- exact match
- normalized exact match
- precision/recall/F1 for span extraction
- numeric tolerance for amounts
- field completeness

A document can be "mostly correct" while one critical field is systematically wrong.

---

# 15. Predictive-model validation

The test set should approximate the intended real-world prediction problem.

## Prefer temporal holdout when

The model is meant to predict future outcomes.

Example:

Train: 2010–2020  
Validate: 2021–2022  
Test: 2023–2024

Avoid random splitting if it puts future regimes into the training set.

## Regression metrics

- MAE
- RMSE
- out-of-sample \(R^2\)

## Classification metrics

- ROC-AUC
- PR-AUC
- F1
- precision/recall
- calibration

Compare against simple benchmarks.

---

# 16. Calibration

If predicted probabilities will be interpreted as risk or used in downstream analysis, check calibration.

Methods:

- reliability plot
- calibration intercept/slope
- Brier score

A model can rank observations well but produce poorly calibrated probabilities.

---

# 17. Leakage audit

Run this audit before accepting strong performance.

Check whether:

- the same firm appears across train/test;
- near-identical text appears across splits;
- duplicated regulatory templates appear across splits;
- future observations influenced vocabulary;
- future documents entered novelty/similarity reference sets;
- labels incorporate future outcomes;
- preprocessing was fit on the full corpus before splitting;
- manually coded examples used for prompt/model tuning leaked into evaluation.

If yes, redesign the split or pipeline.

---

# 18. Domain-shift validation

Test whether the measure works across:

- time periods
- industries
- firm size
- document sources
- regulatory regimes
- writing styles

A model trained on large industrial firms may fail on financial firms or small issuers.

Report performance by economically relevant subgroup when feasible.

---

# 19. Robustness across methods

When the construct is novel, compare against at least one alternative measurement strategy.

Examples:

- dictionary vs LLM
- TF-IDF similarity vs embeddings
- LDA vs BERTopic
- logit vs BERT
- GPT-style classifier vs open-source Transformer

The goal is not identical results. The goal is to understand which findings are method-dependent.

---

# 20. Robustness across aggregation

If text-level predictions are converted into firm-year variables, test plausible alternatives.

Examples:

- any-positive indicator
- count
- proportion
- weighted severity
- maximum score
- number of distinct categories
- entropy/diversity

State which aggregation best matches the theoretical construct.

---

# 21. Sample-size logic for annotation

There is no universal gold-set size.

Choose size based on:

- number of classes
- rarity
- desired precision of performance estimates
- expected disagreement
- model-development needs

Practical principle:

> Collect enough labeled examples that each economically important class has a meaningful number of true positive cases in the held-out test set.

For rare classes, oversample likely positives for annotation, but evaluate with metrics and weighting that respect the intended population.

---

# 22. Confidence intervals

Where feasible, report uncertainty around model-performance estimates.

Options:

- bootstrap confidence intervals
- binomial intervals for proportions
- repeated cross-validation for model comparison

This is especially useful when the gold set is modest.

---

# 23. Model comparison

Do not compare models only by the single best metric.

Consider:

- validity
- stability
- cost
- speed
- reproducibility
- interpretability
- scalability
- licensing/data constraints
- domain transfer

The "best" production method for a paper may not be the model with the highest F1 if the gain is trivial and reproducibility is substantially worse.

---

# 24. Validation table for a paper

A useful validation table might contain:

| Measure / Model | Precision | Recall | F1 | Macro-F1 | Human agreement | Notes |
|---|---:|---:|---:|---:|---:|---|

For topic discovery, use a separate table:

| Model | Topics | Outlier share | Stability | Human coherence | External validity |
|---|---:|---:|---:|---:|---:|

Do not force unlike models into one metric.

---

# 25. Suggested appendix materials

For novel computational measures, include or archive:

- construct definition
- annotation codebook
- examples of positive/negative cases
- prompt templates
- model names/versions
- hyperparameters
- split logic
- confusion matrix
- class-level metrics
- error taxonomy
- robustness results
- aggregation rules
- reproducibility information

---

# 26. Minimum validation standards by method

## Dictionary
Minimum:
- manual positive/negative sample review
- precision/recall or equivalent error assessment
- dictionary sensitivity

## Embedding measure
Minimum:
- human pairwise validation
- alternative embedding model
- reference-set sensitivity

## Topic model
Minimum:
- stability analysis
- human interpretation
- representative and random document inspection
- external/economic validation

## Supervised classifier
Minimum:
- clean held-out test
- leakage audit
- class-level metrics
- error analysis

## LLM measure
Minimum:
- explicit codebook
- held-out human gold set
- prompt/model robustness
- logged model/version/prompt
- error analysis

## Predictive ML
Minimum:
- out-of-sample benchmark
- appropriate temporal/group split
- calibration where probabilities matter

## Causal ML
Minimum:
- credible identification independent of ML
- overlap diagnostics
- sensitivity / robustness
- clear distinction between nuisance prediction and causal target

---

# 27. Reviewer questions to preempt

Before submission, be able to answer:

1. Why is this measure valid?
2. Who defined the construct?
3. How were labels created?
4. How much do human coders agree?
5. How does the model perform by class?
6. What errors does it make?
7. Could leakage explain the performance?
8. Does it generalize across time and industries?
9. Are results robust to another model or prompt?
10. Why use this method instead of a simpler alternative?
11. How is document-level output aggregated?
12. Can the measure be reproduced later?

---

# 28. Validation workflow template

Use this sequence:

```text
1. Define construct
2. Define unit
3. Draft codebook
4. Pilot human coding
5. Revise and freeze codebook
6. Create development/validation/test partitions
7. Fit baseline
8. Fit preferred method
9. Tune only on development/validation data
10. Evaluate once on held-out test
11. Perform error analysis
12. Run robustness / alternative-model checks
13. Test economic/external validity
14. Freeze measurement pipeline
15. Apply to full corpus
16. Aggregate to final empirical variable
17. Document provenance
```

---

# 29. Final rule

Validation should answer two separate questions:

> **Does the model reproduce the coding rule?**

and

> **Does the coding rule validly represent the economic construct?**

High predictive performance addresses only the first.
