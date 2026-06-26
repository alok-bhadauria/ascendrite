# Ascendrite Revision Layer: Production Feature Engineering

## 1. Target Encoding with Laplace Smoothing

Prevents overfitting on rare category variables by interpolating category means with the global dataset average:
$$S_i = \lambda(n_i) \bar{y}_i + (1 - \lambda(n_i)) \mu_y$$

where:
*   $\bar{y}_i$ is the target mean of category $i$.
*   $\mu_y$ is the global target mean.
*   $n_i$ is the occurrence count of category $i$.
*   $\lambda(n_i)$ is the weighting function:
    $$\lambda(n_i) = \frac{n_i}{n_i + m}$$
    where $m$ is the smoothing regularizer parameter.

---

## 2. Feature Selection: Mutual Information

Measures non-linear shared information between variables using KL divergence:
$$I(X; Y) = \sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y) \log_2 \left( \frac{p(x, y)}{p(x)p(y)} \right)$$

*   If $X$ and $Y$ are independent: $I(X; Y) = 0$.
*   Captures non-linear dependencies (unlike Pearson correlation).

---

## 3. L1 vs. L2 Constraints and Projections

*   **L1 (LASSO):** Diamond-shaped constraint boundary ($\|\boldsymbol{\beta}\|_1 \le t$). Intersections with loss contours occur at corners along coordinate axes, setting coefficients to exactly zero (inducing sparsity).
*   **L2 (Ridge):** Circular constraint boundary ($\|\boldsymbol{\beta}\|_2^2 \le t$). Coefficients are shrunk but rarely set to exactly zero.
*   **PCA (Linear):** Rotates dimensions along directions of maximum variance. Preserves global relationships.
*   **t-SNE (Non-Linear):** Minimizes KL divergence of pairwise distances. Suitable for visualization but does not support mapping new samples.
*   **UMAP (Non-Linear):** Based on Riemannian manifolds. Faster than t-SNE, preserves global structure better, and supports mapping new samples.
