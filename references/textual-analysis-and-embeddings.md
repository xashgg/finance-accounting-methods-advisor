# Textual Analysis and Embeddings
## Finance & Accounting Methods Advisor

Use this file when the research problem involves financial/accounting text such as:

- 10-K / 10-Q filings
- annual reports
- MD&A
- risk factors
- SEC comment letters
- earnings-call transcripts
- analyst reports
- shareholder / CEO / chairman letters
- ESG/sustainability reports
- patents
- corporate news
- audit reports

The objective is to convert text into a **defensible research construct**, not merely to produce embeddings or topics.

---

# 1. Start from the construct

Before coding, complete:

```text
Construct:
Why text contains evidence about it:
Text source:
Modeling unit:
Final econometric unit:
Known categories or unknown themes?
Lexical or semantic construct?
Time-respecting reference set required?
```

Examples:

```text
Construct: semantic novelty of risk-factor disclosure
Source: 10-K Item 1A
Unit: risk-factor paragraph
Final unit: firm-year
Task: semantic similarity / novelty
Reference set: prior filings only
```

```text
Construct: types of SEC accounting concerns
Source: SEC correspondence
Unit: individual SEC comment
Final unit: firm-year
Task: discovery first, classification second
```

---

# 2. Text-unit selection

The unit of text is often more important than the model.

Prefer economically meaningful units:

- filing section
- risk factor
- paragraph
- sentence
- SEC comment
- analyst question
- management answer
- audit matter
- patent abstract/claim
- press-release paragraph

Avoid complete-document modeling when a document contains multiple unrelated constructs.

## Multi-topic documents

If one letter contains several accounting issues, document-level topic assignment can be misleading.

Possible remedies:

- split at natural comment boundaries;
- split by paragraph;
- use multilabel classification;
- use sentence/chunk-level inference and aggregate.

---

# 3. Preprocessing philosophy

Do not apply aggressive preprocessing automatically.

For modern semantic models, usually preserve:

- punctuation
- negation
- numbers when economically meaningful
- accounting terminology
- sentence structure

Potentially remove:

- HTML/navigation artifacts
- repeated headers/footers
- signatures/salutations
- filing boilerplate unrelated to the construct
- duplicated blocks

For classical TF-IDF/LDA, preprocessing choices may matter more.

Always document:

- lowercase policy
- stopwords
- stemming/lemmatization
- number treatment
- n-grams
- boilerplate removal
- minimum document frequency

---

# 4. Dictionary measurement

Use dictionaries when the construct is sufficiently lexical.

## Appropriate examples

- explicit AI mentions
- standard references such as ASC 606
- cybersecurity terminology
- litigation keywords
- forward-looking markers
- financial tone dictionaries

## Finance/accounting lesson

General-language dictionaries can misclassify financial terminology. Domain validity must be checked.

Core reference:

Loughran, T., & McDonald, B. (2011).  
"When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks."  
*Journal of Finance*, 66(1), 35–65.  
https://doi.org/10.1111/j.1540-6261.2010.01625.x

## Minimal Python

```python
import re

patterns = {
    "ai": re.compile(r"\b(artificial intelligence|machine learning|generative ai)\b", re.I),
    "cyber": re.compile(r"\b(cybersecurity|cyber attack|data breach)\b", re.I),
}

def dictionary_flags(text: str) -> dict:
    return {name: int(bool(pattern.search(text))) for name, pattern in patterns.items()}
```

## Validation

Use a human-coded sample and estimate:

- precision
- recall
- false-positive types
- false-negative types

---

# 5. TF-IDF and lexical similarity

Use when the construct concerns wording, reuse, copying, boilerplate, or lexical change.

## Minimal workflow

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.95,
)

X = vectorizer.fit_transform(documents)
S = cosine_similarity(X)
```

## Research design choices

Specify:

- corpus used to fit vocabulary
- n-gram range
- min/max document frequency
- stopwords
- document segmentation
- reference set

## Leakage warning

For novelty at time \(t\):

```text
reference corpus = documents available before t
```

Do not fit a "novelty" benchmark using future documents if the construct is intended to represent contemporaneous novelty.

---

# 6. Semantic embeddings

Sentence embeddings are appropriate when semantically equivalent text can use different words.

Official Sentence Transformers documentation describes embeddings as fixed-size representations useful for semantic textual similarity, semantic search, clustering, classification, and retrieval workflows.

Documentation:
https://www.sbert.net/

## Core workflow

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

emb = model.encode(
    documents,
    normalize_embeddings=True,
    show_progress_bar=True,
    batch_size=64,
)
```

With normalized embeddings:

```python
similarity = emb @ emb.T
```

## Do not choose a model from popularity alone

Consider:

- intended task
- language
- financial-domain vocabulary
- maximum input length
- model license
- computational cost
- evidence from a pilot human-validation set

Benchmark at least one alternative embedding model for a novel research construct.

---

# 7. Semantic similarity design

Typical measure:

\[
Similarity_{ij}
=
\cos(e_i,e_j)
\]

Possible research variables:

## Disclosure persistence

\[
Persistence_{it} =
Similarity(Text_{it}, Text_{i,t-1})
\]

## Semantic novelty

\[
Novelty_{it}
=
1-\max_{j \in \mathcal{I}_{t-1}}Similarity(Text_{it},Text_j)
\]

where \(\mathcal{I}_{t-1}\) contains only prior information.

## Concept proximity

\[
ConceptScore_i = Similarity(Text_i, ConceptPrototype)
\]

Prototype may be:

- a validated definition
- averaged embeddings of positive exemplars
- multiple concept exemplars

Prefer multiple validated exemplars over one arbitrary sentence when possible.

---

# 8. Validate embedding measures

If similarity is a research construct:

1. sample pairs across score quantiles;
2. blind human coders to model scores;
3. have humans rate semantic similarity;
4. calculate rank/linear association;
5. inspect high-score false positives;
6. inspect low-score false negatives;
7. repeat with an alternative model.

Possible human scale:

```text
0 = unrelated
1 = weakly related
2 = moderately related
3 = strongly equivalent
```

Store pair IDs and coder judgments.

---

# 9. Long-text embeddings

Do not silently truncate annual reports or long sections.

Options:

## Natural segmentation

Preferred:
- section
- paragraph
- risk factor
- comment
- Q&A turn

## Chunking

If necessary:

```text
chunk length
overlap
boundary rule
aggregation
```

Aggregation strategies:

- mean embedding
- max concept similarity
- top-k mean
- attention/weighted aggregation
- proportion above a threshold

The aggregation must match the construct.

---

# 10. Retrieval before classification

For huge corpora, retrieval can reduce cost.

Example:

> Find candidate paragraphs related to AI investment before applying an expensive LLM classifier.

Workflow:

```text
corpus
  ↓
sparse/dense retrieval
  ↓
top-k candidates
  ↓
reranking
  ↓
LLM / human coding
```

Sentence Transformers supports a common bi-encoder → reranker architecture.

Possible evaluation:

- Recall@k
- Precision@k
- human relevance

Use a high-recall first stage when missing positives is costly.

---

# 11. Sparse vs dense retrieval

## Sparse: BM25 / keyword

Strong when:
- terminology is specific;
- exact phrases matter;
- transparency matters.

## Dense embeddings

Strong when:
- synonyms/paraphrases matter;
- concepts can be expressed indirectly.

## Hybrid

Often appropriate:

```text
BM25 score + dense retrieval score
```

Then rerank the candidate set.

---

# 12. Topic discovery: LDA/NMF

Use if the taxonomy is not yet known.

## LDA

Strengths:
- established literature
- topic mixtures
- interpretable word distributions

Weaknesses:
- bag-of-words assumptions
- sensitive to preprocessing and \(K\)
- weaker semantic representation

## NMF

Works well with TF-IDF and often yields interpretable factors.

Example:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

tfidf = TfidfVectorizer(min_df=10, ngram_range=(1, 2))
X = tfidf.fit_transform(documents)

nmf = NMF(n_components=20, random_state=42)
W = nmf.fit_transform(X)
H = nmf.components_
```

Do not select \(K\) using one automated metric only.

---

# 13. BERTopic

BERTopic's current default architecture is modular:

```text
embeddings
  ↓
UMAP
  ↓
HDBSCAN
  ↓
c-TF-IDF
  ↓
topic representation
```

Official documentation:
https://maartengr.github.io/BERTopic/

The package allows individual components to be replaced, so a "BERTopic result" is not one immutable model specification.

## Minimal workflow

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

topic_model = BERTopic(
    embedding_model=embedding_model,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)

topic_info = topic_model.get_topic_info()
representatives = topic_model.get_representative_docs()
```

## Important

UMAP introduces stochasticity unless controlled, and HDBSCAN density settings affect topic count/granularity.

Save:

- embedding model
- UMAP parameters
- HDBSCAN parameters
- vectorizer
- random state where applicable
- corpus version

---

# 14. Topic-model robustness grid

For a publishable discovery study, consider a compact grid rather than unlimited tuning.

Example:

```text
Embedding models: 2
Minimum cluster sizes: 3 values
UMAP neighbor settings: 2 values
Time subsamples: 2
```

Evaluate whether major economic themes persist.

Avoid selecting the single run that "looks best" without a prespecified interpretation protocol.

---

# 15. Topic interpretation protocol

For each major topic provide coders:

1. top terms;
2. representative documents;
3. random assigned documents;
4. no model-generated label initially.

Ask:

```text
What common issue appears?
Is the topic coherent?
Should it merge?
Should it split?
What proportion of sampled documents fit the label?
```

Then compare coder labels.

An LLM may assist with naming after human inspection, but should not substitute for validation.

---

# 16. Discovery → production measurement

Recommended workflow:

```text
unsupervised discovery
       ↓
domain interpretation
       ↓
stable taxonomy
       ↓
annotation codebook
       ↓
human gold labels
       ↓
supervised classifier
       ↓
held-out validation
       ↓
full-corpus classification
```

This is usually more reproducible than using unsupervised topic assignments as final firm-year variables.

---

# 17. Text classification baseline

Always consider:

```text
TF-IDF + logistic regression
TF-IDF + linear SVM
```

Example:

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

clf = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=5,
        max_features=100_000,
    )),
    ("model", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
    )),
])

clf.fit(X_train, y_train)
```

These baselines are inexpensive and interpretable.

---

# 18. Transformer classification

Use when contextual semantics materially improve classification.

Common families:

- BERT
- RoBERTa
- DeBERTa
- domain-adapted models

Official Hugging Face Transformers documentation:
https://huggingface.co/docs/transformers/

## Research rules

Do not merely report training loss.

Report:

- split design
- class distribution
- hyperparameter logic
- held-out class-level metrics
- confusion matrix
- leakage audit
- error taxonomy

For corporate filings, consider firm-group or temporal test sets.

---

# 19. Multi-label classification

Finance/accounting passages often contain several issues.

Example SEC comment:

```text
revenue recognition
+ segment disclosure
+ internal control
```

Do not force single-label coding if the economics is multilabel.

Use:

```text
one binary output per category
```

Validate each category separately.

---

# 20. Temporal drift

Language changes over time because of:

- regulation
- new accounting standards
- technology
- crises
- disclosure fashion
- boilerplate evolution

Test:

```text
train early → test late
```

and/or report performance by period.

If later language materially degrades performance, consider:

- periodic relabeling
- fine-tuning
- updated exemplars
- dynamic dictionaries

---

# 21. Aggregating text outputs

Possible paragraph/comment → firm-year variables:

## Extensive margin

\[
AnyIssue_{it}=1[\text{at least one positive passage}]
\]

## Intensive margin

\[
ShareIssue_{it}
=
\frac{\# positive passages}{\# passages}
\]

## Diversity

\[
DistinctIssues_{it}
=
\#\{\text{predicted categories}\}
\]

## Semantic novelty

mean / max / upper-tail distance to prior reference texts.

Do not choose an aggregation only because it gives stronger regressions.

---

# 22. Storage architecture

Recommended:

```text
data/raw/
data/parsed/
data/chunks/
data/embeddings/
data/predictions/
data/validation/
data/final/
```

Each modeled text row should preserve:

```text
document_id
firm_id
date
section
chunk_id
raw_text_hash
processed_text
model_version
prediction
score
run_id
```

Keep embeddings outside CSV for large projects; use Parquet/NumPy/vector storage as appropriate.

---

# 23. Reproducible embedding cache

Pseudo-pattern:

```python
from pathlib import Path
import numpy as np
import pandas as pd

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Save metadata separately
meta = pd.DataFrame({
    "row_id": ids,
    "model": MODEL_NAME,
})

np.save("data/embeddings/embeddings.npy", emb)
meta.to_parquet("data/embeddings/metadata.parquet", index=False)
```

Do not rely on row order without persistent IDs.

---

# 24. Recommended references

## Core conceptual

Gentzkow, M., Kelly, B., & Taddy, M. (2019).  
"Text as Data." *Journal of Economic Literature*, 57(3), 535–574.  
https://doi.org/10.1257/jel.20181020

## Accounting/Python

Anand, V., Bochkay, K., Chychyla, R., & Leone, A. J. (2020).  
"Using Python for Text Analysis in Accounting Research."  
*Foundations and Trends in Accounting*, 14(3–4), 128–359.

## Financial dictionaries

Loughran, T., & McDonald, B. (2011).  
"When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks."  
*Journal of Finance*, 66(1), 35–65.

## Official implementation resources

Sentence Transformers:
https://www.sbert.net/

BERTopic:
https://maartengr.github.io/BERTopic/

Hugging Face Transformers:
https://huggingface.co/docs/transformers/

scikit-learn:
https://scikit-learn.org/

---

# 25. Publication checklist

Before using a text-derived variable in a main regression, verify:

- [ ] construct defined before model choice
- [ ] unit of analysis justified
- [ ] corpus construction documented
- [ ] preprocessing documented
- [ ] baseline estimated
- [ ] modern method justified
- [ ] leakage checked
- [ ] human validation performed
- [ ] error analysis performed
- [ ] temporal/domain robustness checked
- [ ] aggregation justified
- [ ] model/version recorded
- [ ] code can regenerate final variable

---

# 26. Final rule

Choose the representation that matches the construct:

> **lexical construct → lexical methods**

> **semantic construct → embeddings/contextual models**

> **unknown structure → discovery**

> **known taxonomy → classification**

Do not use topic modeling when the real question is classification, and do not use semantic models when simple rules already measure the construct reliably.
