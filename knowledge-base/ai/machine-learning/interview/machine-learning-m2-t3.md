# Ascendrite Interview Prep: Data Quality & Advanced Imputation

## Q1: Explain the difference between MAR and MNAR, and why this distinction matters in production.

### Standard Answer
*   **MAR (Missing at Random):** The probability of a data point being missing depends on observed variables. For instance, in a medical survey, younger individuals might be less likely to fill out heart rate logs. If we control for age, the missingness becomes random. We can impute MAR data successfully using MICE or regression models.
*   **MNAR (Missing Not at Random):** The probability of missingness depends directly on the unobserved value itself. For instance, users with poor credit ratings are less likely to report their credit scores. If we impute MNAR scores using standard observed sample means, we introduce severe positive bias.

### Interview Trap
Interviewers will ask: "How do you test if your dataset is MAR or MNAR?"
The correct response is that you cannot distinguish MAR and MNAR using quantitative data tests alone, since the values are missing. Resolving MNAR requires explicit modeling of the selection bias (e.g., Heckman correction) or qualitative tracking of the data collection process.

---

## Q2: Why is Euclidean distance unsuitable for multivariate outlier detection, and how does Mahalanobis distance resolve this?

### Standard Answer
Euclidean distance treats all coordinate dimensions as orthogonal (uncorrelated) and scaled identically. If features are highly correlated (e.g., height and weight), Euclidean distance does not capture the directional variance, leading to two major issues:
1.  **Spherical Assumption:** Outlier boundaries are treated as spheres, whereas correlated data distributions are ellipsoids.
2.  **Scale Sensitivity:** Features with larger numerical ranges dominate the distance calculation.

Mahalanobis distance resolves this by incorporating the inverse covariance matrix:
$$D_M(\mathbf{x}) = \sqrt{(\mathbf{x} - \boldsymbol{\mu})^{\top} \mathbf{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})}$$
This scales and rotates the coordinate space to account for variances and cross-correlations, transforming the elliptical distribution into a spherical space where outliers can be detected accurately.

---

## Q3: What is the risk of performing mean imputation on a continuous feature?

### Standard Answer
Mean imputation introduces two major statistical anomalies:
1.  **Underestimation of Variance:** Replacing missing cells with the mean artificially squeezes the variance of the distribution.
2.  **Correlation Distortion:** It forces the covariance between the imputed feature and other features toward zero, destroying the multivariate relationships needed by regression or tree algorithms.
