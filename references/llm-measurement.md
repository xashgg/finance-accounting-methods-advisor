# LLM Measurement
## Finance & Accounting Methods Advisor

Use this file when a research construct will be measured, coded, classified, extracted, scored, or annotated with a generative large language model.

The central rule is:

> **Treat the LLM as a measurement instrument, not as an oracle.**

LLMs are especially useful when the target construct requires semantic judgment that can be expressed in a detailed coding protocol.

---

# 1. Appropriate research tasks

Strong candidates include:

- classify SEC comments into accounting issues
- identify managerial evasiveness
- distinguish firm-specific from macro uncertainty
- identify strategic framing
- extract reasons for capital-allocation decisions
- identify AI use cases from disclosures
- code whether a response answers an analyst's question
- extract structured event attributes
- classify nuanced disclosure themes

Weak candidates include:

- exact keyword presence
- deterministic standard numbers
- stable date/amount formats
- simple entity matching
- constructs where no defensible coding definition exists

Use regex/dictionaries when they solve the task more reliably.

---

# 2. Required construct specification

Before prompting, write a codebook.

Minimum:

```text
Construct name:
Conceptual definition:
Unit of analysis:
Positive inclusion rules:
Negative exclusion rules:
Ambiguous cases:
Multilabel rules:
Evidence requirement:
Output scale:
Aggregation rule:
```

Example:

```text
Construct:
Revenue-recognition regulatory concern

Code positive if:
The regulator questions timing, performance obligations,
consideration, principal-agent treatment, collectability,
disaggregation tied to recognition, or another issue that
materially affects recognition of reported revenue.

Code negative if:
Revenue is mentioned only descriptively, as a segment statistic,
as growth commentary, or in an unrelated receivables discussion.
```

If humans cannot consistently apply the codebook, model performance is not the main problem.

---

# 3. Separate prompt development from evaluation

Use distinct datasets:

```text
pilot/development set
        ↓
prompt construction

validation set
        ↓
model/prompt/threshold selection

held-out test set
        ↓
final reported performance
```

Do not repeatedly inspect the test-set errors and then report the same test metrics as unbiased evaluation.

---

# 4. Human gold labels

For novel constructs:

1. pilot-code examples;
2. refine definitions;
3. freeze codebook;
4. independently label the gold set;
5. report human agreement;
6. resolve/adjudicate only according to a predefined process.

Gold data should contain:

- difficult cases
- negative cases
- rare categories
- different industries/years
- different text lengths

Do not validate only on obvious positives.

---

# 5. Zero-shot vs few-shot vs supervised

## Zero-shot

Use when:
- category definition is clear;
- examples are scarce;
- you need a fast pilot.

Risk:
- model interprets categories differently from researchers.

## Few-shot

Use when:
- boundary cases matter;
- good exemplars clarify the coding policy.

Examples should represent coding rules, not merely easy cases.

## Supervised fine-tuning / conventional classifier

Prefer when:
- labeled data are sufficiently large;
- the task is stable;
- inference volume is large;
- cost/reproducibility matters.

LLM classification can remain a benchmark or annotation assistant.

---

# 6. Prompt structure

Prefer explicit sections.

```text
ROLE
You are applying a research coding protocol.

CONSTRUCT
...

INCLUSION RULES
...

EXCLUSION RULES
...

AMBIGUOUS CASES
...

INPUT
...

OUTPUT SCHEMA
...
```

Avoid vague prompts such as:

```text
Is this disclosure innovative?
```

unless "innovative" is operationally defined.

---

# 7. Structured output

Prefer JSON or schema-validated outputs.

Example:

```json
{
  "label": 1,
  "category": "revenue_recognition",
  "evidence": "short supporting excerpt or rationale",
  "confidence": 0.91
}
```

For production datasets, store:

- parsed fields
- raw model response
- request ID/run ID
- model identifier
- prompt version
- timestamp

Do not let malformed responses silently become missing values.

---

# 8. Evidence fields

When appropriate, ask the model to return a compact evidence field.

Benefits:

- easier error auditing
- easier human review
- easier detection of keyword shortcuts

But:

> model-generated evidence is not independent validation.

The gold label remains the anchor.

---

# 9. Chain-of-thought policy for research pipelines

Do not design the workflow around collecting hidden model reasoning.

For reproducible research, prefer observable outputs:

- label
- evidence span
- short justification
- extracted fields
- confidence/category score when meaningful

The research instrument should be auditable from inputs and recorded outputs without requiring private internal reasoning.

---

# 10. Model choice

Select models based on:

- coding accuracy on the gold set
- stability
- cost
- throughput
- context window
- data-governance constraints
- version reproducibility
- structured-output support

Do not select a model from leaderboard prestige alone.

For a paper, a slightly weaker but stable/reproducible model may be preferable to a marginally stronger opaque setup.

---

# 11. Model comparison

A strong design may compare:

```text
human coding
dictionary baseline
TF-IDF classifier
Transformer classifier
LLM classifier
```

Not every project needs all five.

Choose comparisons that reveal whether the LLM adds semantic value.

---

# 12. Evaluation metrics

For classification:

- precision
- recall
- F1
- per-class metrics
- confusion matrix
- macro-F1 for multiclass
- PR-AUC for rare binary classes

For extraction:

- exact match
- normalized exact match
- field-level precision/recall/F1
- numeric tolerance

For ordinal scores:

- weighted agreement
- rank correlation
- calibration against humans

---

# 13. Prompt robustness

Test reasonable alternative formulations.

Examples:

- concise vs detailed codebook
- example ordering
- with/without few-shot examples
- alternative but equivalent wording

Do not perform unlimited prompt search.

Prespecify a small robustness set and report whether substantive results depend on the prompt.

---

# 14. Model robustness

If feasible, compare at least one alternative model family for a novel construct.

The goal is not identical labels.

Ask:

- does aggregate prevalence change materially?
- do class-level errors differ?
- do downstream coefficients depend on model choice?
- are disputed observations concentrated in one subgroup?

---

# 15. Stochasticity

For stochastic generation:

- control temperature when possible;
- record generation settings;
- test repeatability on a subset;
- consider repeated classification for unstable cases.

If deterministic/near-deterministic settings are available and appropriate, prefer them for measurement.

Do not hide irreducible instability.

---

# 16. Confidence

LLM self-reported confidence is not automatically calibrated probability.

Do not interpret:

```json
{"confidence": 0.95}
```

as a statistically calibrated 95% probability without validation.

If confidence is used:

- validate calibration;
- compare with actual accuracy;
- use it primarily for triage unless calibrated.

---

# 17. Human-in-the-loop design

Useful production workflow:

```text
LLM classifies all observations
       ↓
high-confidence routine cases
       ↓
accept under validated rule

low-confidence / conflicting cases
       ↓
human review
```

But the threshold must be validated.

Do not allow human intervention to depend on downstream regression outcomes.

---

# 18. Active learning

When manual labels are expensive:

1. label an initial random/diverse sample;
2. fit a provisional classifier;
3. identify uncertain/boundary cases;
4. label additional cases;
5. preserve a separate untouched test set.

Active learning improves training efficiency but can distort prevalence if active-learning samples are treated as population samples.

---

# 19. Multi-label constructs

Many financial passages contain multiple concepts.

Use multilabel output when conceptually appropriate:

```json
{
  "revenue_recognition": 1,
  "segment_reporting": 1,
  "internal_control": 0
}
```

Avoid forcing one "main topic" if multiple issues are substantively relevant.

---

# 20. Ordinal scoring

For constructs such as severity:

```text
0 = none
1 = minor
2 = moderate
3 = severe
```

Provide explicit anchors for every level.

Validate:

- adjacent-level confusion
- human agreement
- monotonicity with external indicators

Do not ask the LLM for a 0–100 score without anchors unless a continuous scale is theoretically justified.

---

# 21. Continuous constructs

If using continuous LLM scores:

1. define what one unit means;
2. provide anchors;
3. check test-retest stability;
4. compare against human ratings;
5. inspect score distribution;
6. validate ranking and calibration.

Often, ordinal categories are more defensible than arbitrary continuous scores.

---

# 22. Information extraction

Prefer structured extraction when the target consists of factual fields.

Example schema:

```json
{
  "accounting_issue": "string",
  "standard": "string|null",
  "amount_usd": "number|null",
  "fiscal_period": "string|null",
  "firm_response_requested": "string|null"
}
```

Validate each field independently.

---

# 23. Long documents

Do not send entire long filings merely because the model context permits it.

Reasons:

- multiple constructs
- increased cost
- attention dilution
- weak unit definition

Prefer:

```text
retrieve relevant passages
       ↓
classify/extract
       ↓
aggregate
```

Use section boundaries and paragraph-level units when possible.

---

# 24. Retrieval-augmented measurement

When classification requires external rules or standards:

```text
target passage
+ relevant accounting/regulatory guidance
       ↓
LLM coding
```

Potentially useful for:

- accounting-standard interpretation
- regulation-specific coding
- rule changes over time

But avoid contaminating historical measurement with guidance unavailable at that historical date when the construct is contemporaneous perception/knowledge.

---

# 25. Temporal consistency

Model versions and prompts can change.

For longitudinal datasets:

- freeze the model where possible;
- run the entire corpus under one model version;
- if re-running after a model change, measure disagreement;
- record inference dates.

Do not classify early years with one prompt/model and later years with another unless intentionally modeled and validated.

---

# 26. Cost strategy

For millions of observations:

## Option A — LLM directly

Best if:
- corpus is manageable;
- semantic judgment is highly complex.

## Option B — LLM labels training data

```text
human-validated LLM annotations
       ↓
smaller supervised model
       ↓
full corpus
```

Useful for scale, but validate the final model against independent human labels.

## Option C — retrieve then LLM

Use a cheap high-recall filter before expensive inference.

---

# 27. Reproducibility record

For every inference run save:

```text
run_id
model_provider
model_name
model_version/snapshot if exposed
request_date
prompt_version
system_prompt_hash
user_template_hash
few_shot_version
temperature
top_p
max_output_tokens
schema_version
source_text_id
raw_response
parsed_response
parse_status
retry_count
```

Also preserve code commit/environment.

---

# 28. Error taxonomy

Common LLM measurement failures:

- instruction misinterpretation
- overly literal coding
- category overlap
- hallucinated factual extraction
- excessive use of general knowledge
- wrong accounting meaning
- insufficient context
- over-broad context
- negation failure
- historical/regulatory mismatch
- output-schema failure

Report examples in an appendix for novel measures.

---

# 29. Downstream regression sensitivity

After validating the labeler, test whether major empirical results are robust to:

- human labels on the validation sample
- alternative prompt
- alternative model
- alternative classification threshold
- dictionary/conventional classifier benchmark
- excluding ambiguous observations

Do not optimize the coding method based on which version gives the preferred economic coefficient.

---

# 30. Core methodological reference

de Kok, T. (2025).  
"ChatGPT for Textual Analysis? How to Use Generative LLMs in Accounting Research."  
*Management Science*, 71(9), 7888–7906.  
https://doi.org/10.1287/mnsc.2023.03253

The paper emphasizes that generative LLMs expand the set of textual-analysis tasks available to accounting researchers but introduce due-diligence and validity requirements.

Companion repository:
https://github.com/TiesdeKok/chatgpt_paper

---

# 31. Companion references

Gentzkow, M., Kelly, B., & Taddy, M. (2019).  
"Text as Data." *Journal of Economic Literature*, 57(3), 535–574.  
https://doi.org/10.1257/jel.20181020

Anand, V., Bochkay, K., Chychyla, R., & Leone, A. J. (2020).  
"Using Python for Text Analysis in Accounting Research."

Use the skill's validation guidelines for gold-set design and error analysis.

---

# 32. Minimal LLM measurement template

```text
Research construct:
Unit:
Output type:
Classes/scale:
Inclusion rules:
Exclusion rules:
Ambiguous cases:
Gold sample:
Human agreement:
Development set:
Validation set:
Test set:
Model:
Prompt version:
Structured output:
Metrics:
Error taxonomy:
Prompt robustness:
Model robustness:
Aggregation:
Downstream robustness:
```

---

# 33. Paper reporting template

Report:

## Construct development
- theoretical definition
- coding protocol
- unit of analysis

## Human annotation
- coders
- training
- codebook
- agreement
- adjudication

## LLM procedure
- model
- version/date
- prompt
- examples
- structured schema
- settings

## Validation
- test-set design
- metrics
- confusion matrix
- errors
- robustness

## Variable construction
- aggregation
- missing/failed outputs
- ambiguity handling

## Reproducibility
- code/prompts
- model identifiers
- archived outputs where licensing permits

---

# 34. Final rule

An LLM-based variable is defensible when:

> **the construct is independently defined, humans can apply the coding rule, the model reproduces that rule on held-out data, errors are understood, results are robust to reasonable measurement alternatives, and the entire instrument is reproducible.**

The fact that an LLM can produce an answer is not evidence that the answer is a valid research measure.
