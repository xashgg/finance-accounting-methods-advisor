# Validation Protocol
## ML / NLP / LLM Research Measure

> Use this template to preregister or document how a computational measure will be validated.

---

# 1. Measure

**Measure name**

> [Name]

**Construct**

> [Definition]

**Method**

> [Dictionary / TF-IDF / embedding / classifier / LLM / topic model / prediction model.]

**Unit**

> [Unit]

---

# 2. Validation Questions

This protocol must answer:

1. Does the computational method reproduce the intended coding rule?
2. Does that coding rule validly represent the economic construct?
3. Does performance generalize across relevant firms, industries, and periods?
4. Is the measure robust to reasonable implementation choices?

---

# 3. Gold Standard

**Gold-label source**

> [Human coding / authoritative external database / observed outcome.]

**Sample size**

> [N]

**Sampling method**

- [ ] Random
- [ ] Stratified
- [ ] Oversample rare positives
- [ ] Confidence-stratified
- [ ] Time-stratified
- [ ] Industry-stratified

**Sampling strata**

> [Describe.]

---

# 4. Data Partition

```text
development:
validation:
test:
```

Test set must remain untouched until final evaluation.

**Split level**

> [Firm / time / document / row.]

**Leakage controls**

> [Describe.]

---

# 5. Primary Metrics

## Classification

- [ ] Precision
- [ ] Recall
- [ ] F1
- [ ] Macro-F1
- [ ] PR-AUC
- [ ] ROC-AUC
- [ ] Confusion matrix

## Regression / scoring

- [ ] MAE
- [ ] RMSE
- [ ] Correlation with human score
- [ ] Rank correlation
- [ ] Calibration

## Extraction

- [ ] Exact match
- [ ] Field-level F1
- [ ] Numeric tolerance accuracy

## Topic discovery

- [ ] Stability
- [ ] Human coherence
- [ ] Topic diversity
- [ ] External validity

**Primary success metric**

> [Metric + target.]

---

# 6. Human Agreement

**Coders**

> [N]

**Metric**

> [Kappa / alpha / percent agreement.]

**Target**

> [Threshold.]

**Disagreement policy**

> [Adjudication.]

---

# 7. Error Analysis

Review at least:

```text
false positives:
false negatives:
high-confidence errors:
low-confidence correct cases:
rare classes:
long texts:
short texts:
different industries:
different time periods:
```

Create an error taxonomy.

| Error type | Count | Example | Planned response |
|---|---:|---|---|
| [Type] | | | |

---

# 8. Construct Validity

## Convergent validity

Compare against:

> [Existing measure.]

Expected relationship:

> [Direction/strength.]

## Discriminant validity

Show measure is distinct from:

- [Neighboring construct 1]
- [Neighboring construct 2]

## Economic/external validity

Expected patterns:

1. [Prediction]
2. [Prediction]
3. [Prediction]

---

# 9. Robustness Across Methods

Primary method:

> [Method]

Alternatives:

1. [Alternative 1]
2. [Alternative 2]
3. [Alternative 3]

Compare:

- prevalence
- agreement
- class-level errors
- downstream coefficients

Do not select the method based on preferred downstream significance.

---

# 10. Robustness Across Parameters

Test only substantively reasonable alternatives:

```text
thresholds:
embedding model:
prompt:
LLM model:
chunk size:
topic hyperparameters:
classifier hyperparameters:
```

Prespecify the compact grid where possible.

---

# 11. Temporal / Domain Generalization

Report performance by:

- [ ] time period
- [ ] industry
- [ ] firm size
- [ ] document source
- [ ] regulatory regime
- [ ] language

Flag material degradation.

---

# 12. Threshold Selection

If a threshold is needed:

**Selection data**

> Validation set only.

**Criterion**

- [ ] Maximize F1
- [ ] Minimum precision
- [ ] Minimum recall
- [ ] Research-specific loss
- [ ] Other

**Frozen threshold**

> [Value.]

---

# 13. Confidence Intervals

Method:

- [ ] Bootstrap
- [ ] Binomial interval
- [ ] Repeated CV
- [ ] Other

Report uncertainty for key performance statistics when feasible.

---

# 14. Aggregation Validation

If predictions are aggregated:

Test:

- [ ] any-positive
- [ ] count
- [ ] proportion
- [ ] max
- [ ] average
- [ ] diversity/entropy

Preferred aggregation:

> [Choice + theoretical reason.]

---

# 15. Reproducibility

Archive:

- raw IDs
- labels
- codebook
- prompts
- model/version
- package environment
- seeds
- data split
- thresholds
- errors
- run logs
- final variable construction code

---

# 16. Acceptance Criteria

The measure is accepted for full-sample inference only if:

- [ ] Human agreement is adequate
- [ ] Primary metric meets target
- [ ] No severe leakage is detected
- [ ] Major error modes are understood
- [ ] Results generalize reasonably
- [ ] Construct validity is supported
- [ ] Alternative methods do not reveal a fatal dependence
- [ ] Reproducibility package is complete

If not, revise the construct or measurement process rather than merely tuning the model.
