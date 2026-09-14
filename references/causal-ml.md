# Causal Machine Learning
## Finance & Accounting Methods Advisor

Use this file when the user proposes machine learning for causal inference, heterogeneous treatment effects, flexible nuisance estimation, or treatment-effect prediction.

The central rule is:

> **Machine learning can improve estimation; it cannot create identification.**

---

# 1. First classify the research goal

Distinguish:

## Prediction

> Which firms will adopt AI?

Target:
\[
E[Y|X]
\]

## Association

> How is AI adoption associated with performance conditional on controls?

Still not necessarily causal.

## Causal effect

> What is the effect of AI adoption on performance?

Target:
\[
E[Y(1)-Y(0)]
\]

## Heterogeneous causal effect

> Which firms benefit more from AI adoption?

Target:
\[
\tau(X)=E[Y(1)-Y(0)|X]
\]

Only the last two require a causal identification strategy.

---

# 2. Identification before algorithms

Before recommending DML or causal forests, write:

```text
Treatment:
Outcome:
Treatment timing:
Outcome timing:
Population:
Identification strategy:
Confounders:
Potential post-treatment variables:
Panel structure:
Clustering level:
Overlap/common support:
```

If identification is not credible, do not proceed as though causal ML solves the problem.

---

# 3. Common finance/accounting identification settings

Potential designs include:

- selection on observables / unconfoundedness
- difference-in-differences
- instrumental variables
- regression discontinuity
- randomized/natural experiments
- panel fixed effects
- event studies

Causal ML may complement some of these designs, but the assumptions remain design-specific.

---

# 4. When Double/Debiased ML is useful

DML is useful when:

- the causal target is low-dimensional;
- nuisance functions are high-dimensional/flexible;
- regularized ML is useful for predicting outcome/treatment;
- orthogonal scores and cross-fitting can reduce regularization/overfitting bias.

The DoubleML documentation implements the double/debiased ML framework and emphasizes orthogonalization plus sample splitting/cross-fitting.

Official documentation:
https://docs.doubleml.org/

Core reference:

Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E.,
Hansen, C., Newey, W., & Robins, J. (2018).
"Double/Debiased Machine Learning for Treatment and Structural Parameters."
*The Econometrics Journal*, 21(1), C1–C68.
https://doi.org/10.1111/ectj.12097

---

# 5. Intuition for DML

Suppose:

\[
Y = \theta D + g(X) + \varepsilon
\]

and treatment:

\[
D = m(X) + v
\]

Flexible ML can estimate:

\[
\hat g(X), \hat m(X)
\]

Then residualization/orthogonalization isolates variation less sensitive to nuisance-estimation error.

Cross-fitting prevents an observation from being evaluated with nuisance predictions trained on that same observation.

The goal is not better prediction for its own sake; prediction is used to estimate nuisance functions supporting causal inference.

---

# 6. DML workflow

Generic workflow:

```text
define causal target
      ↓
define nuisance functions
      ↓
choose ML learners
      ↓
sample splitting
      ↓
fit nuisance models
      ↓
orthogonal score
      ↓
cross-fitting
      ↓
causal estimate + inference
```

Do not manually reproduce this if a well-tested library covers the design.

---

# 7. DoubleML Python starting point

Illustrative structure:

```python
import doubleml as dml
from sklearn.ensemble import RandomForestRegressor

# df must include:
# outcome y
# treatment d
# covariates x1...xp

data = dml.DoubleMLData(
    df,
    y_col="y",
    d_cols="d",
    x_cols=covariates,
)

ml_l = RandomForestRegressor(
    n_estimators=500,
    min_samples_leaf=10,
    random_state=42,
)

ml_m = RandomForestRegressor(
    n_estimators=500,
    min_samples_leaf=10,
    random_state=42,
)

model = dml.DoubleMLPLR(
    data,
    ml_l=ml_l,
    ml_m=ml_m,
    n_folds=5,
)

model.fit()
print(model.summary)
```

Exact model/learner choices depend on treatment type and estimand.

Consult current documentation before implementation.

---

# 8. Nuisance learner selection

Candidate learners:

- LASSO / elastic net
- random forest
- gradient boosting
- neural networks

Selection should be based on nuisance predictive quality and stability, not causal coefficient preference.

Where feasible:

- tune within training folds;
- use cross-fitting;
- report learner robustness.

Do not tune nuisance models using the sign/significance of the treatment effect.

---

# 9. Cross-fitting

Cross-fitting is central to DML.

Conceptually:

```text
Fold A:
train nuisance models on B,C,D,E
predict nuisance functions on A

repeat for all folds
```

Then construct orthogonal scores from out-of-fold nuisance predictions.

Do not compute nuisance predictions in-sample and call the result DML.

---

# 10. Clustered and panel data

Finance/accounting datasets often have:

- repeated firm observations
- industry shocks
- year shocks
- cluster dependence

Random row-level cross-fitting may leak firm-specific patterns.

Consider whether splitting should respect:

- firm
- time
- treatment assignment unit

Inference must also reflect appropriate clustering.

Do not assume standard package defaults match a panel research design.

---

# 11. Treatment timing

For an adoption treatment:

```text
pre-adoption covariates
        ↓
treatment/adoption
        ↓
post-treatment outcomes
```

Do not include variables caused by adoption as pre-treatment controls.

Text measures can themselves be post-treatment.

Example:

If annual-report "AI disclosure" rises because of actual AI adoption, controlling for disclosure after adoption may block part of the treatment effect.

---

# 12. Selection on observables

DML under unconfoundedness still assumes that treatment is conditionally as-if random given observed \(X\).

ML flexibility does not address:

- unobserved managerial quality
- omitted strategy
- endogenous adoption timing
- reverse causality

If these remain plausible, state the limitation or use a stronger design.

---

# 13. Overlap

Check whether treated and control firms have comparable covariates/treatment propensity.

Problems:

- near-deterministic treatment
- propensity near 0 or 1
- treatment concentrated in one industry/time period

Possible responses:

- redefine population
- trimming
- overlap weights
- narrower estimand

Do not extrapolate heterogeneous effects where support is weak.

---

# 14. Heterogeneous treatment effects

Use when heterogeneity is a substantive research question.

Examples:

- AI adoption works differently by human capital
- regulation effects differ by information environment
- financing intervention effects vary by constraint level

Do not search thousands of heterogeneity dimensions without theory or correction.

---

# 15. Causal forests

Useful for flexible conditional treatment effects.

Core outputs may include:

- individual/CATE estimates
- subgroup effects
- variable importance for heterogeneity

Important:

"important for heterogeneity" is not the same as "causes the treatment effect."

Use honest sample splitting/inference methods where supported.

---

# 16. EconML

EconML provides ML-based estimators for heterogeneous treatment effects, including orthogonal/double-ML families.

Official documentation:
https://econml.azurewebsites.net/

Before using an estimator, determine:

- treatment continuous/binary/multivalued?
- outcome type?
- instrument?
- unconfoundedness?
- target CATE/ATE?
- inference needs?

Do not select estimator classes from package names alone.

---

# 17. Heterogeneity workflow

Recommended:

```text
theory predicts moderators
       ↓
estimate overall ATE
       ↓
estimate CATE / group effects
       ↓
validate heterogeneity
       ↓
report interpretable subgroups
```

Avoid starting with a black-box CATE model and mining whatever subgroup appears strongest.

---

# 18. Honest heterogeneity tests

Possible strategies:

- train CATE model in one sample;
- form high/low predicted-effect groups;
- estimate group treatment effects in separate/held-out data;
- test monotonicity across predicted-effect bins.

This reduces overfitting of treatment-effect heterogeneity.

---

# 19. Difference-in-differences and ML

Do not replace a DiD design with generic DML.

First address:

- treatment timing
- staggered adoption
- parallel trends
- anticipation
- treatment-effect dynamics
- appropriate comparison groups

ML can help with nuisance estimation or heterogeneity after the DiD identification structure is clear.

Current DoubleML documentation includes DiD model support; consult the package guide before implementation.

---

# 20. Instrumental variables and ML

If using IV:

You still need:

- relevance
- exclusion
- independence/as-if random instrument
- monotonicity where LATE interpretation is used

ML can estimate flexible first-stage/nuisance functions but does not make an invalid instrument valid.

---

# 21. RDD and ML

For regression discontinuity:

Do not replace local identification with global random forests.

Preserve:

- cutoff logic
- bandwidth reasoning
- continuity assumptions
- manipulation tests

Flexible methods may supplement, not erase, design logic.

---

# 22. Fixed effects + ML

High-dimensional firm/year effects create complications.

Ask:

- Is the treatment identified within firm?
- Are nuisance models respecting panel structure?
- Are fixed effects preprocessed appropriately?
- Does sample splitting leak firm identity?

A standard cross-sectional causal-ML recipe may be inappropriate.

---

# 23. Text as covariates

Text-derived covariates can enter causal ML.

Examples:

- disclosure embeddings
- business-description embeddings
- managerial language
- analyst questions

But ask:

- is the text measured before treatment?
- could text encode treatment/outcome leakage?
- does dimension reduction preserve causal timing?
- are embeddings fit using future corpus information?

Use time-respecting text construction.

---

# 24. Text as treatment

If treatment is constructed from LLM/text classification:

Example:

```text
AI adoption treatment =
LLM-classified evidence of operational AI adoption
```

Then causal validity depends on both:

1. treatment measurement validity;
2. causal identification validity.

Misclassification can bias treatment-effect estimates.

Validate the treatment measure independently before causal estimation.

---

# 25. Text as outcome

Example:

> Does regulation change disclosure complexity?

If the outcome is an ML/LLM-derived text score:

- validate the score;
- ensure model behavior is stable across treatment groups and time;
- test whether treatment changes wording in ways that affect measurement mechanically.

Measurement invariance matters.

---

# 26. Causal forests vs interaction regressions

Use theory-driven interaction regressions when:

- moderators are few and prespecified;
- functional form is plausible;
- interpretability is central.

Use causal forests when:

- heterogeneity is high-dimensional/nonlinear;
- discovering effect patterns is part of the research objective;
- sufficient sample size/support exists.

A causal forest is not automatically superior.

---

# 27. DML vs conventional regression

DML is attractive when:

- nuisance relationships are complex/high-dimensional;
- regularization is needed;
- the causal target remains low-dimensional.

Conventional regression may be preferable when:

- controls are modest and theory-driven;
- sample size is limited;
- functional form is transparent;
- DML adds little beyond complexity.

Always explain why ML is needed.

---

# 28. Diagnostics

Depending on design, inspect:

- treatment share
- propensity distribution
- overlap
- nuisance out-of-fold performance
- residual distributions
- fold balance
- sensitivity to learner class
- sensitivity to folds/seeds
- subgroup sample sizes
- time/industry support

Poor nuisance prediction is informative but high nuisance prediction alone does not prove identification.

---

# 29. Learner robustness

For a novel DML application, consider:

```text
LASSO
random forest
gradient boosting
```

If causal estimates change drastically by nuisance learner, investigate:

- overlap
- misspecification
- small sample
- instability
- regularization
- data leakage

Do not choose the learner giving the desired coefficient.

---

# 30. Hyperparameter tuning

Nested tuning is preferable when feasible:

```text
outer cross-fitting folds
    ↓
inner tuning within training data
```

Never tune using the held-out causal outcome in a way that contaminates the target estimate.

Use computationally parsimonious grids.

---

# 31. Standard errors and inference

Use inference appropriate to:

- DML estimator
- clustering
- repeated observations
- treatment assignment
- panel/time structure

Do not manually attach OLS standard errors to arbitrary ML treatment-effect predictions.

Use library-supported inference when assumptions fit.

---

# 32. Multiple testing in heterogeneity

If testing many groups/moderators:

- prespecify key moderators;
- correct/acknowledge multiplicity;
- distinguish confirmatory from exploratory heterogeneity.

Do not turn causal ML into unrestricted subgroup fishing.

---

# 33. Reporting template

## Research design
- treatment
- outcome
- timing
- population
- identification assumptions

## Causal ML role
- estimand
- nuisance functions
- why ML is needed
- learner classes

## Cross-fitting
- number of folds
- split unit
- tuning
- seeds

## Diagnostics
- overlap
- nuisance performance
- support

## Inference
- standard errors
- clustering
- confidence intervals

## Robustness
- alternative learners
- conventional specification
- alternative samples
- alternative treatment/outcome construction

## Heterogeneity
- prespecified vs exploratory
- held-out validation
- subgroup support

---

# 34. Core references

## DML

Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E.,
Hansen, C., Newey, W., & Robins, J. (2018).  
"Double/Debiased Machine Learning for Treatment and Structural Parameters."  
*The Econometrics Journal*, 21(1), C1–C68.  
https://doi.org/10.1111/ectj.12097

## Economists and ML

Athey, S., & Imbens, G. W. (2019).  
"Machine Learning Methods That Economists Should Know About."  
*Annual Review of Economics*, 11, 685–725.  
https://doi.org/10.1146/annurev-economics-080217-053433

## Software

DoubleML:
https://docs.doubleml.org/

EconML:
https://econml.azurewebsites.net/

DoubleML Python implementation paper:

Bach, P., Chernozhukov, V., Kurz, M. S., & Spindler, M. (2022).  
"DoubleML — An Object-Oriented Implementation of Double Machine Learning in Python."  
*Journal of Machine Learning Research*, 23(53), 1–6.

---

# 35. Decision template

```text
Causal question:
Treatment:
Outcome:
Timing:
Identification strategy:
Estimand:
Why conventional method is insufficient:
Why ML is needed:
Nuisance functions:
Learners:
Cross-fitting plan:
Overlap diagnostics:
Cluster structure:
Heterogeneity target:
Robustness learners:
Conventional benchmark:
```

---

# 36. Red flags

Stop and reconsider if the proposal is:

> "Use XGBoost to prove X causes Y."

> "Use causal forest because the treatment is endogenous."

> "Use SHAP values as causal mechanisms."

> "Control for every variable available, including post-treatment variables."

> "Use all annual-report text, including post-treatment disclosures, as treatment predictors."

> "Randomly split a panel without checking firm/time leakage."

> "Search hundreds of moderators and report the strongest CATE."

These are design problems, not tuning problems.

---

# 37. Final rule

Use causal ML only when you can explain this chain:

> **causal estimand → identification assumptions → timing → nuisance functions → ML role → orthogonal/cross-fit estimation → diagnostics → inference → robustness**

If the identification assumptions fail, a more sophisticated learner does not rescue the causal claim.
