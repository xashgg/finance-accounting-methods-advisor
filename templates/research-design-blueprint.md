# Research Design Blueprint
## Finance & Accounting Computational Methods

> Use this template when converting a research question into a complete computational empirical design.

---

# 1. Research Question

**Primary question**

> [State the substantive finance/accounting research question.]

**Economic motivation**

> [Why does this question matter theoretically or empirically?]

**Target contribution**

- [ ] New construct / measure
- [ ] New data
- [ ] New empirical setting
- [ ] New causal evidence
- [ ] New prediction task
- [ ] New heterogeneity evidence
- [ ] Methodological contribution
- [ ] Other: __________

---

# 2. Construct Definition

**Main construct**

> [Define the economic/accounting construct in one precise sentence.]

**Why the available data contain evidence about the construct**

> [Explain the mapping from raw data/text to the construct.]

**Construct type**

- [ ] Observable
- [ ] Latent
- [ ] Text-derived
- [ ] Model-derived
- [ ] Treatment
- [ ] Outcome
- [ ] Moderator
- [ ] Control
- [ ] Instrument
- [ ] Prediction target

**Potential neighboring constructs that must be distinguished**

- [Construct A]
- [Construct B]
- [Construct C]

---

# 3. Data

**Primary source**

> [SEC, annual reports, earnings calls, Compustat, CRSP, analyst reports, etc.]

**Sample period**

> [YYYY–YYYY]

**Population**

> [e.g., U.S. public firms; Chinese A-share firms.]

**Raw unit**

> [Document / filing / paragraph / comment / Q&A turn / firm-year / event.]

**Final empirical unit**

> [Firm-year / firm-quarter / event / observation.]

**Identifiers**

```text
firm_id:
date:
document_id:
subdocument_id:
other keys:
```

**Expected sample filters**

- [Filter 1]
- [Filter 2]
- [Filter 3]

---

# 4. Computational Task Type

Select the primary task:

- [ ] Dictionary / rule-based measurement
- [ ] Lexical similarity
- [ ] Semantic similarity
- [ ] Topic discovery
- [ ] Supervised classification
- [ ] LLM classification
- [ ] Information extraction
- [ ] Prediction
- [ ] Retrieval
- [ ] Anomaly detection
- [ ] Causal ML
- [ ] Other: __________

**Why this task family matches the research objective**

> [Explain.]

---

# 5. Unit of Analysis

**Preferred modeling unit**

> [e.g., individual SEC comment.]

**Why this unit is economically appropriate**

> [Explain.]

**Alternative units considered**

| Alternative | Why not preferred |
|---|---|
| [Whole document] | [Reason] |
| [Paragraph] | [Reason] |
| [Sentence] | [Reason] |

**Chunking required?**

- [ ] No
- [ ] Yes

If yes:

```text
chunk boundary:
chunk length:
overlap:
aggregation:
```

---

# 6. Measurement / Modeling Strategy

## Baseline

**Method**

> [e.g., TF-IDF + logistic regression.]

**Why this baseline is credible**

> [Explain.]

## Preferred method

**Method**

> [e.g., DeBERTa classifier / BERTopic / sentence embeddings / LLM.]

**Why preferred**

> [Explain the specific limitation of the baseline that this method addresses.]

## Serious alternative

**Method**

> [Alternative.]

**Why it remains plausible**

> [Explain.]

---

# 7. Training / Reference Data

**Human labels available?**

- [ ] Yes
- [ ] No
- [ ] Will be created

**Gold-standard construction**

> [Describe coder sample and procedure.]

**Data split**

```text
training:
validation:
test:
```

**Split unit**

- [ ] Random row
- [ ] Firm
- [ ] Time
- [ ] Document family
- [ ] Industry
- [ ] Other: __________

**Why this split avoids leakage**

> [Explain.]

---

# 8. Validation Plan

## Measurement validity

- [ ] Human gold labels
- [ ] Inter-rater reliability
- [ ] Precision / recall / F1
- [ ] Error analysis
- [ ] Convergent validity
- [ ] Discriminant validity
- [ ] Economic/external validity

## Topic discovery

- [ ] Coherence/diversity
- [ ] Stability across seeds
- [ ] Stability across hyperparameters
- [ ] Human interpretation
- [ ] External validity

## Prediction

- [ ] Out-of-sample performance
- [ ] Temporal holdout
- [ ] Calibration
- [ ] Simple benchmark

**Primary validation criterion**

> [State the criterion that determines whether the measure/model is acceptable.]

---

# 9. Leakage Audit

Check each:

- [ ] Same firm across train/test
- [ ] Adjacent-year boilerplate
- [ ] Near-duplicate text
- [ ] Repeated templates
- [ ] Future vocabulary
- [ ] Future reference documents
- [ ] Outcome leakage
- [ ] Post-treatment controls
- [ ] Prompt/test contamination
- [ ] Human-label contamination

**Mitigation**

> [Describe.]

---

# 10. Aggregation to Research Variables

If the model operates below the empirical unit:

**Passage-level output**

> [label / score / embedding / probability]

**Aggregation**

- [ ] Any-positive indicator
- [ ] Count
- [ ] Proportion
- [ ] Average
- [ ] Maximum
- [ ] Number of distinct categories
- [ ] Entropy/diversity
- [ ] Weighted severity
- [ ] Other: __________

**Economic interpretation**

> [What exactly does the resulting firm-year variable mean?]

---

# 11. Main Econometric Design

**Dependent variable**

> [Variable.]

**Key explanatory variable / treatment**

> [Variable.]

**Baseline specification**

\[
Y_{it} = \alpha + \beta X_{it} + \Gamma Controls_{it} + FE + \varepsilon_{it}
\]

**Fixed effects**

- [ ] Firm
- [ ] Year
- [ ] Industry
- [ ] Industry × year
- [ ] Other: __________

**Standard-error clustering**

> [Firm / industry / two-way / etc.]

**Causal identification**

> [If causal, state the identifying assumption/design.]

---

# 12. Robustness Plan

## Measurement robustness

- [Alternative dictionary]
- [Alternative embedding model]
- [Alternative classifier]
- [Alternative LLM]
- [Alternative prompt]
- [Alternative threshold]
- [Alternative chunking]
- [Alternative aggregation]

## Econometric robustness

- [Alternative controls]
- [Alternative FE]
- [Alternative clustering]
- [Alternative sample]
- [Placebo]
- [Lead/lag]
- [Alternative outcome]
- [Alternative treatment]

---

# 13. Expected Tables and Figures

## Main paper

- Table 1: Sample construction / descriptive statistics
- Table 2: Validation / model performance
- Table 3: Main regressions
- Table 4: Robustness / heterogeneity
- Figure 1: Research design / construct pipeline
- Figure 2: Time / distribution / validation visualization

## Appendix

- Annotation codebook
- Confusion matrix
- Error examples
- Hyperparameters
- Prompt
- Alternative model results
- Additional validation

---

# 14. Reproducibility

Record:

```text
data acquisition date:
raw-data version:
code commit:
environment:
model:
model version:
prompt version:
random seed:
train/validation/test IDs:
annotation version:
aggregation version:
```

---

# 15. Reviewer Risk Assessment

**Most likely reviewer concern**

> [Concern.]

**Why it matters**

> [Explain.]

**Planned response**

> [Validation/robustness/design change.]

Repeat for 3–5 major risks.

---

# 16. Go / No-Go Criteria

Proceed to full-sample modeling only if:

- [ ] Construct definition is stable
- [ ] Unit is justified
- [ ] Gold sample is adequate
- [ ] Validation meets target
- [ ] Major leakage risks are resolved
- [ ] Measure has economic interpretation
- [ ] Main method outperforms or materially improves on baseline
- [ ] Reproducibility record is complete
