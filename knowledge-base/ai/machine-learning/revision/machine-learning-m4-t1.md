# Ascendrite Revision Layer: Generalization Theory & Overfitting

## 1. Bias-Variance Decomposition

Expected prediction error of a model $\hat{f}(\mathbf{x})$ under squared error loss, where true target $y = f(\mathbf{x}) + \epsilon$, $\mathbb{E}[\epsilon] = 0$, and $\text{Var}(\epsilon) = \sigma^2$:

$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \text{Bias}[\hat{f}(\mathbf{x})]^2 + \text{Var}[\hat{f}(\mathbf{x})] + \sigma^2$$

*   **Bias (Systematic Error):** $\text{Bias}[\hat{f}(\mathbf{x})] = \mathbb{E}[\hat{f}(\mathbf{x})] - f(\mathbf{x})$. Measures error from simplified assumptions (causes underfitting).
*   **Variance (Sensitivity):** $\text{Var}[\hat{f}(\mathbf{x})] = \mathbb{E}[(\hat{f}(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2]$. Measures sensitivity to training data fluctuations (causes overfitting).
*   **Irreducible Error:** $\sigma^2$ (noise variance).

---

## 2. Empirical Risk & Rademacher Complexity

### Risks
*   **Empirical Risk (Training Loss):** $R_{\text{emp}}(h) = \frac{1}{N} \sum_{i=1}^N \mathcal{L}(h(\mathbf{x}_i), y_i)$
*   **True Risk (Generalization Loss):** $R(h) = \mathbb{E}_{(\mathbf{x}, y) \sim \mathcal{D}} [\mathcal{L}(h(\mathbf{x}), y)]$

### Empirical Rademacher Complexity
Measures hypothesis class capacity to fit random labels $\sigma_i \in \{-1, 1\}$:
$$\hat{\mathcal{R}}_S(\mathcal{H}) = \mathbb{E}_{\boldsymbol{\sigma}} \left[ \sup_{h \in \mathcal{H}} \frac{1}{N} \sum_{i=1}^N \sigma_i h(\mathbf{x}_i) \right]$$
*   *Generalization Bound:* With probability $\ge 1-\delta$, $R(h) \le R_{\text{emp}}(h) + 2 \hat{\mathcal{R}}_S(\mathcal{H}) + 3 \sqrt{\frac{\log(2/\delta)}{2N}}$.

---

## 3. Vapnik-Chervonenkis (VC) Dimension

*   **Shattering:** A hypothesis class $\mathcal{H}$ shatters set $S$ if it can realize all $2^{|S|}$ binary labelings on $S$.
*   **VC Dimension $d_{\text{VC}}$:** Largest cardinality of a set that $\mathcal{H}$ can shatter.
    *   *Linear Classifiers:* In $\mathbb{R}^2$ $d_{\text{VC}} = 3$. In $\mathbb{R}^d$ $d_{\text{VC}} = d + 1$.
*   *VC Generalization Bound:* With probability $\ge 1-\delta$,
    $$R(h) \le R_{\text{emp}}(h) + \sqrt{\frac{8 d_{\text{VC}} \log\left(\frac{2e N}{d_{\text{VC}}}\right) + 8 \log(4/\\delta)}{N}}$$
*   **Regularization link:** Penalizing weight magnitudes directly constrains Rademacher complexity, bounding generalization error: $\hat{\mathcal{R}}_S(\mathcal{H}_{L_2}) \le \frac{B \max_i \|\mathbf{x}_i\|_2}{\sqrt{N}}$.
