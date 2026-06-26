# Ascendrite Revision Layer: Data Quality & Advanced Imputation

## 1. Missing Data Mechanisms

*   **MCAR (Missing Completely at Random):** Missingness probability is independent of any data:
    $$P(M \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(M)$$
*   **MAR (Missing at Random):** Missingness probability depends on observed data but not missing values:
    $$P(M \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(M \mid Y_{\text{obs}})$$
*   **MNAR (Missing Not at Random):** Missingness probability depends on the unobserved missing value itself:
    $$P(M \mid Y_{\text{obs}}, Y_{\text{mis}}) \neq P(M \mid Y_{\text{obs}})$$

---

## 2. Advanced Imputation Formulation

### KNN Imputation (Distance-Weighted)
Sample distance weight:
$$w_r = \frac{1}{d(\mathbf{x}_i, \mathbf{x}_r)}$$

Imputed missing feature value:
$$x_{i,j} = \frac{\sum_{r=1}^k w_r x_{r,j}}{\sum_{r=1}^k w_r}$$

### MICE (Multivariate Imputation by Chained Equations)
An iterative regression-based solver. Loops through each missing feature $Y_j$, predicting it using a model trained on all other features $\mathbf{Y}_{-j}$. Typically stabilizes within 10 to 20 cycles.

---

## 3. Out-of-Distribution Outliers

### Mahalanobis Distance
Unlike Euclidean distance, Mahalanobis distance incorporates the inverse covariance matrix to scale and rotate coordinate axes:
$$D_M(\mathbf{x}) = \sqrt{(\mathbf{x} - \boldsymbol{\mu})^{\top} \mathbf{\Sigma}^{-1} (\\mathbf{x} - \boldsymbol{\mu})}$$

### Chi-Squared Distribution
The square of the distance follows a Chi-squared distribution:
$$D_M^2(\mathbf{x}) \sim \chi^2_d$$
where $d$ is the dimensionality of the vector space. Thresholds are set using Chi-squared lookup limits.
