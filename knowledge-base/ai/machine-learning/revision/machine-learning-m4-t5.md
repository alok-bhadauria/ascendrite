# Ascendrite Revision Layer: Boosting Algorithms & Tree Libraries

## 1. Functional Gradient Descent & AdaBoost

Boosting fits weak learners sequentially to minimize loss in function space: $F_t(\mathbf{x}) = F_{t-1}(\mathbf{x}) + \beta_t h_t(\mathbf{x})$.

### AdaBoost (Adaptive Boosting)
Minimizes Exponential Loss $\mathcal{L}_{\text{exp}}(y, F(\mathbf{x})) = e^{-y F(\mathbf{x})}$ for $y_i, h_t(\mathbf{x}_i) \in \{-1, 1\}$:
*   **Weighted Error Rate:** $\epsilon_m = \frac{\sum_{i=1}^N w_i^{(m)} \mathbb{I}(y_i \neq h_m(\mathbf{x}_i))}{\sum_{i=1}^N w_i^{(m)}}$
*   **Model Weight:** $\beta_m = \frac{1}{2} \log\left( \frac{1 - \epsilon_m}{\epsilon_m} \right)$
*   **Sample Weight Update:** $w_i^{(m+1)} = w_i^{(m)} e^{-y_i \beta_m h_m(\mathbf{x}_i)}$
*   *Limitation:* Outlier sensitivity due to exponential penalty growth.

---

## 2. Second-Order Gradient Boosting (XGBoost)

Approximates general loss via second-order Taylor expansion:

$$\mathcal{L}^{(t)} \approx \sum_{i=1}^N \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2$$
where $g_i = \frac{\partial \mathcal{L}}{\partial \hat{y}^{(t-1)}}$ (gradient) and $h_i = \frac{\partial^2 \mathcal{L}}{\partial (\hat{y}^{(t-1)})^2}$ (Hessian).

### Optimal Parameters
*   **Optimal Leaf Weight:** $w_j^* = -\frac{G_j}{H_j + \lambda}$, where $G_j = \sum_{i \in I_j} g_i$ and $H_j = \sum_{i \in I_j} h_i$.
*   **Optimal Structure Score:** $\tilde{\mathcal{L}}^{(t)}(q) = -\frac{1}{2} \sum_{j=1}^T \frac{G_j^2}{H_j + \lambda} + \gamma T$
*   **Split Gain Formula:** $\text{Gain} = \frac{1}{2} \left[ \frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{G_P^2}{H_P + \lambda} \right] - \gamma$
*   *Pruning constraint:* Split occurs only when $\text{Gain} > 0$. Regularization L2 is $\lambda$, L1 threshold is $\gamma$.

---

## 3. LightGBM vs. CatBoost Architectures

### LightGBM
*   **Leaf-wise Growth:** Splits leaf that maximizes loss reduction, creating asymmetric, deep trees.
*   **Histograms:** Groups continuous features into integer bins (e.g., 256) to accelerate split-scanning.
*   **GOSS & EFB:** Gradient-based One-Side Sampling and Exclusive Feature Bundling.

### CatBoost
*   **Symmetric Oblivious Trees:** Same split condition across an entire level of the tree. Inference runs at hardware speeds via bitwise indexing.
*   **Ordered Boosting:** Calculates gradients on permutations of the dataset independent of split searches, resolving target leakage/prediction shift.
*   **Target Encoding:** High-cardinality categoricals encoded symmetrically during splits.
