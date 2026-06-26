# Ascendrite Revision Layer: Bagging & Random Forests

## 1. Bootstrap Aggregation (Bagging)

Given dataset $\mathcal{D}$ of size $N$, draw $B$ bootstrap samples of size $N$ with replacement. Fit model $h_b$ on each.

### Prediction Aggregation
*   **Regression:** $h_{\text{bag}}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^B h_b(\mathbf{x})$
*   **Classification:** Majority vote of $\{h_b(\mathbf{x})\}_{b=1}^B$

### Ensemble Variance Formula
Let predictions $X_i$ have variance $\sigma^2$ and correlation $\rho > 0$. For ensemble average $Y = \frac{1}{B} \sum_{i=1}^B X_i$:
$$\text{Var}(Y) = \rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2$$
*   **Variance Limit:** $\lim_{B \to \infty} \text{Var}(Y) = \rho \sigma^2$.
*   **Key Insight:** Ensemble variance is lower-bounded by tree correlation $\rho$. Bagging does not reduce bias, only variance.

---

## 2. Out-of-Bag (OOB) Estimation

*   **Exclude Probability:** Probability of a sample $\mathbf{x}_i$ being omitted from a bootstrap set of size $N$ over $N$ draws:
    $$p = \left( 1 - \frac{1}{N} \right)^N \implies \lim_{N \to \infty} p = e^{-1} \approx 0.368$$
    *   *Result:* $\approx 36.8\%$ of data is left Out-of-Bag (OOB) for any tree.
*   **OOB Error Protocol:** Predict $\mathbf{x}_i$ using only the subset of trees that did not see $\mathbf{x}_i$ during training. The average loss across all samples provides an unbiased estimate of generalization error.

---

## 3. Random Forests

Reduces tree correlation $\rho$ to lower the variance bound $\rho\sigma^2$.

### Feature Subspace Sampling
At each node split, randomly select $m$ features from the total $d$ features, and split only on the best candidate within this subset.
*   **Classification Trees:** $m = \sqrt{d}$
*   **Regression Trees:** $m = \frac{d}{3}$
*   *Overfitting:* Increasing the number of trees $B$ does not cause overfitting; it only helps converge the variance to its mathematical limit $\rho\sigma^2$.
