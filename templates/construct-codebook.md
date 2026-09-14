# Construct and Annotation Codebook
## Finance & Accounting Computational Research

> Use this template before human annotation, LLM classification, or supervised model training.

---

# 1. Construct

**Construct name**

> [Name]

**Conceptual definition**

> [One concise theoretical definition.]

**Research role**

- [ ] Main independent variable
- [ ] Dependent variable
- [ ] Treatment
- [ ] Moderator
- [ ] Mediator
- [ ] Control
- [ ] Descriptive taxonomy

---

# 2. Unit of Coding

**Unit**

> [Sentence / paragraph / SEC comment / Q&A response / document / event.]

**Context supplied to coder**

> [Only unit / prior sentence / full Q&A / section heading / metadata.]

**Why this amount of context is necessary**

> [Explain.]

---

# 3. Coding Scheme

**Output type**

- [ ] Binary
- [ ] Multiclass
- [ ] Multilabel
- [ ] Ordinal
- [ ] Continuous
- [ ] Structured extraction

---

# 4. Inclusion Rules

Code as positive / category X when:

1. [Rule]
2. [Rule]
3. [Rule]

---

# 5. Exclusion Rules

Do not code as positive / category X when:

1. [Rule]
2. [Rule]
3. [Rule]

---

# 6. Ambiguous Cases

| Situation | Coding rule |
|---|---|
| [Ambiguity 1] | [Rule] |
| [Ambiguity 2] | [Rule] |
| [Ambiguity 3] | [Rule] |

If uncertain after applying the rules:

- [ ] Use "uncertain"
- [ ] Escalate for adjudication
- [ ] Choose best-fitting category
- [ ] Allow multilabel coding

---

# 7. Positive Examples

## Example 1

**Text**

> [Example.]

**Correct code**

> [Label.]

**Why**

> [Short rationale.]

## Example 2

**Text**

> [Example.]

**Correct code**

> [Label.]

**Why**

> [Short rationale.]

---

# 8. Negative Examples

## Example 1

**Text**

> [Example.]

**Correct code**

> [Label.]

**Why not positive**

> [Explain.]

---

# 9. Boundary Examples

Include examples most likely to generate disagreement.

| Text | Correct code | Boundary reason |
|---|---|---|
| [Example] | [Label] | [Reason] |
| [Example] | [Label] | [Reason] |

---

# 10. Multilabel Rules

If multiple constructs can appear simultaneously:

```text
Can multiple labels be assigned? yes/no
Maximum labels:
Hierarchy:
Parent-child constraints:
Mutually exclusive labels:
```

---

# 11. Ordinal Scale Anchors

If ordinal:

| Score | Definition | Anchor example |
|---:|---|---|
| 0 | None | [Example] |
| 1 | Low | [Example] |
| 2 | Moderate | [Example] |
| 3 | High | [Example] |

Avoid unlabeled 1–10 or 0–100 scales unless each region has clear meaning.

---

# 12. Structured Extraction Schema

If extracting fields:

```json
{
  "field_1": "string|null",
  "field_2": "number|null",
  "field_3": "boolean",
  "field_4": ["string"]
}
```

For each field define:

| Field | Meaning | Allowed values | Missing rule |
|---|---|---|---|
| field_1 | [Meaning] | [Values] | [Rule] |

---

# 13. Human Annotation Procedure

**Number of coders**

> [N]

**Coder qualifications**

> [Domain expertise / training.]

**Pilot size**

> [N]

**Main validation size**

> [N]

**Independent coding?**

- [ ] Yes
- [ ] No

**Adjudication process**

> [Procedure.]

---

# 14. Agreement

Planned metric:

- [ ] Percent agreement
- [ ] Cohen's kappa
- [ ] Krippendorff's alpha
- [ ] Weighted kappa
- [ ] Other: __________

Minimum acceptable agreement:

> [Threshold or qualitative criterion.]

If agreement is low:

1. inspect disagreements;
2. revise construct/codebook;
3. retrain coders;
4. repeat pilot.

Do not immediately blame the annotators.

---

# 15. LLM Prompt Mapping

If an LLM applies this codebook, the prompt must include:

- construct definition
- inclusion rules
- exclusion rules
- ambiguity rules
- output schema
- only necessary examples

Prompt version:

```text
prompt_id:
version:
date:
```

---

# 16. Gold-Set Governance

Freeze before final model evaluation:

```text
codebook version:
gold-set version:
adjudication complete:
test-set locked:
```

Do not use final test labels to rewrite the codebook or prompt.

---

# 17. Revision Log

| Version | Date | Change | Reason |
|---|---|---|---|
| 0.1 | [date] | Initial draft | |
| 0.2 | [date] | [Change] | [Pilot disagreement] |
| 1.0 | [date] | Frozen | |
