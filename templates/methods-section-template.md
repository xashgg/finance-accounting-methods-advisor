# Computational Methods Section Template
## Finance / Accounting Paper

> Use this template after the measurement pipeline is frozen. Replace bracketed text with project-specific content. Do not claim validation results that have not been established.

---

# Computational Measure Construction

We construct **[MEASURE NAME]**, a measure of **[CONSTRUCT]**, from **[TEXT/DATA SOURCE]**. The unit of analysis for measurement is **[UNIT]**, because **[ECONOMIC / INSTITUTIONAL JUSTIFICATION]**. We subsequently aggregate the resulting **[LABELS/SCORES]** to the **[FIRM-YEAR / FIRM-QUARTER / EVENT]** level for the empirical analyses.

## Corpus Construction

We obtain **[DOCUMENT TYPE]** from **[SOURCE]** for the period **[START–END]**. We retain **[INCLUSION CRITERIA]** and exclude **[EXCLUSIONS]**. The resulting corpus contains **[N DOCUMENTS]** documents representing **[N FIRMS / OBSERVATIONS]**. We segment each document into **[SEGMENT TYPE]** using **[RULE]**. This produces **[N UNITS]** text units for model estimation and inference.

We remove **[HTML / HEADERS / FOOTERS / OTHER ARTIFACTS]** while preserving **[NEGATION / NUMBERS / ACCOUNTING TERMS / OTHER CONTENT]**. Additional preprocessing includes **[LOWERCASING / TOKENIZATION / N-GRAMS / ETC.]**. Appendix **[X]** reports the full preprocessing procedure.

## Construct Definition and Human Annotation

We define **[CONSTRUCT]** as **[DEFINITION]**. The annotation protocol specifies explicit inclusion and exclusion rules and addresses ambiguous cases such as **[EXAMPLES]**.

**[N]** independent coders annotate a pilot sample of **[N]** observations. After resolving ambiguities and revising the codebook, we freeze the final annotation protocol and independently code a held-out validation sample of **[N]** observations. Inter-coder agreement is **[METRIC = VALUE]**.

The complete codebook and representative positive, negative, and boundary examples appear in Appendix **[X]**.

## Baseline Method

As a transparent benchmark, we estimate **[BASELINE METHOD]**. Specifically, **[DESCRIPTION OF FEATURES / MODEL / PARAMETERS]**. This benchmark captures **[WHAT IT MEASURES WELL]** but is limited by **[WHY THE PREFERRED METHOD MAY IMPROVE]**.

## Preferred Computational Method

Our primary measure uses **[MODEL / METHOD]**. We select this approach because **[METHOD–CONSTRUCT FIT]**. The model processes **[UNIT]** and produces **[OUTPUT]**.

For **[EMBEDDING / TRANSFORMER / LLM]** models, we use **[MODEL NAME AND VERSION]**. We record **[MODEL VERSION / SNAPSHOT / DATE]** and fix **[RELEVANT INFERENCE SETTINGS]** for all observations.

For an LLM-based measure, the prompt contains the frozen construct definition, inclusion and exclusion rules, **[NUMBER]** examples, and a structured output schema. We do not use the test labels to modify the final prompt.

For a supervised model, we partition observations by **[FIRM / TIME / DOCUMENT FAMILY]** into training, validation, and test samples of **[SIZES]** to reduce **[TYPE OF LEAKAGE]**. Hyperparameters are chosen using only **[TRAINING/VALIDATION DATA]**.

## Validation

We evaluate the preferred measure against the held-out human-coded test sample. The primary validation metrics are **[PRECISION / RECALL / F1 / MACRO-F1 / ETC.]**. The preferred model achieves **[RESULTS]**, compared with **[BASELINE RESULTS]** for the benchmark.

We additionally conduct qualitative error analysis by reviewing **[FALSE POSITIVES / FALSE NEGATIVES / HIGH-CONFIDENCE ERRORS]**. The most common errors involve **[ERROR TYPES]**.

To assess construct validity, we examine **[CONVERGENT VALIDITY TEST]**, **[DISCRIMINANT VALIDITY TEST]**, and **[ECONOMIC / EXTERNAL VALIDITY TEST]**. These tests show **[RESULT—ONLY IF ESTABLISHED]**.

## Robustness of Measurement

We evaluate sensitivity to **[ALTERNATIVE MODEL]**, **[ALTERNATIVE PROMPT / THRESHOLD]**, **[ALTERNATIVE EMBEDDING]**, and **[ALTERNATIVE CHUNKING OR AGGREGATION]**. The resulting measures exhibit **[SUMMARY OF ROBUSTNESS]**.

We also evaluate performance across **[TIME / INDUSTRY / FIRM SIZE / REGULATORY REGIME]** to assess domain shift.

## Aggregation

The model operates at the **[PASSAGE / COMMENT / Q&A]** level, whereas our empirical analysis is conducted at the **[FIRM-YEAR]** level. Our primary variable is:

\[
[VARIABLE]_{it}
=
[FORMULA]
\]

This aggregation captures **[ECONOMIC INTERPRETATION]**. We examine **[ALTERNATIVE AGGREGATIONS]** as robustness tests.

## Reproducibility

We archive the annotation codebook, observation identifiers, data partitions, preprocessing code, model and package versions, prompts where applicable, hyperparameters, random seeds, model outputs, and variable-construction code. These materials allow the computational measure to be regenerated from the underlying corpus subject to **[DATA LICENSING / ACCESS RESTRICTIONS]**.

---

# Optional: Topic Discovery Subsection

We first conduct unsupervised topic discovery to identify candidate **[ISSUE / DISCLOSURE]** categories. As a classical benchmark, we estimate **[LDA/NMF]** models over **[RANGE]** candidate topic counts. We then apply **[BERTopic / EMBEDDING CLUSTERING]** using **[EMBEDDING MODEL]**.

We evaluate topic solutions using model diagnostics, stability across **[SEEDS / HYPERPARAMETERS / EMBEDDING MODELS]**, and human review of top terms, representative documents, and randomly selected assigned documents. We do not interpret the algorithmically generated number of clusters as the unique true number of economic constructs. Instead, discovery informs a stable taxonomy that is subsequently measured using **[SUPERVISED / RULE-BASED]** classification.

---

# Optional: LLM Measurement Subsection

We treat the LLM as a coding instrument rather than as a source of ground truth. The model applies a frozen annotation protocol specifying the construct, inclusion and exclusion criteria, ambiguity rules, and structured output. We evaluate the LLM on a held-out human-coded sample and report class-level precision, recall, and F1, together with inter-coder agreement among human annotators.

We assess measurement robustness using **[ALTERNATIVE PROMPTS]** and **[ALTERNATIVE MODELS]**. For reproducibility, we record the model identifier, model/version information available from the provider, prompt version, inference date, generation parameters, output schema, and failure/retry logic.

---

# Optional: Causal ML Subsection

Our causal parameter of interest is **[ATE / ATT / CATE / OTHER]** of **[TREATMENT]** on **[OUTCOME]**. Identification relies on **[ASSUMPTION / DESIGN]** rather than on machine learning itself.

We use **[DML / CAUSAL FOREST / OTHER]** to flexibly estimate **[NUISANCE FUNCTIONS / HETEROGENEOUS EFFECTS]**. We implement **[K]-fold** cross-fitting, with folds defined at the **[FIRM / CLUSTER]** level. Nuisance functions are estimated using **[LEARNERS]**. We examine overlap, nuisance-model performance, and sensitivity to alternative learner classes.

Standard errors are **[CLUSTERED / BOOTSTRAPPED / LIBRARY-SUPPORTED]** at the **[LEVEL]**. We compare estimates with **[CONVENTIONAL SPECIFICATION]** and report **[OVERLAP / HETEROGENEITY / ROBUSTNESS]** diagnostics.

---

# Methods Appendix Checklist

Include:

- corpus construction flow
- annotation codebook
- coder agreement
- split logic
- model/version
- hyperparameters
- prompt where applicable
- confusion matrix
- class-level metrics
- error taxonomy
- robustness models
- aggregation variants
- reproducibility details
