# Ascendrite Interview Prep: Boosting Algorithms & Tree Libraries

## Q1: Derive the optimal step size (classifier coefficient) $\beta_m$ in AdaBoost by minimizing the Exponential Loss.

### Standard Answer
AdaBoost sequentially constructs an additive model $F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \beta_m h_m(\mathbf{x})$, where $y_i, h_m(\mathbf{x}_i) \in \{-1, 1\}$. We minimize the Exponential Loss:
$$\mathcal{L} = \sum_{i=1}^N e^{-y_i F_m(\mathbf{x}_i)} = \sum_{i=1}^N e^{-y_i (F_{m-1}(\mathbf{x}_i) + \beta_m h_m(\mathbf{x}_i))}$$

Let $w_i^{(m)} = e^{-y_i F_{m-1}(\mathbf{x}_i)}$ represent the sample weights at iteration $m$:
$$\mathcal{L} = \sum_{i=1}^N w_i^{(m)} e^{-y_i \beta_m h_m(\mathbf{x}_i)}$$

Split the summation into two parts: correctly classified samples ($y_i h_m(\mathbf{x}_i) = 1$) and incorrectly classified samples ($y_i h_m(\mathbf{x}_i) = -1$):
$$\mathcal{L} = \sum_{y_i = h_m(\mathbf{x}_i)} w_i^{(m)} e^{-\beta_m} + \sum_{y_i \neq h_m(\mathbf{x}_i)} w_i^{(m)} e^{\beta_m}$$

Rewrite the first sum by adding and subtracting $e^{-\beta_m} \sum_{y_i \neq h_m(\mathbf{x}_i)} w_i^{(m)}$:
$$\mathcal{L} = e^{-\beta_m} \sum_{i=1}^N w_i^{(m)} + (e^{\beta_m} - e^{-\beta_m}) \sum_{i=1}^N w_i^{(m)} \mathbb{I}(y_i \neq h_m(\mathbf{x}_i))$$

We define the weighted error rate $\epsilon_m$ as:
$$\epsilon_m = \frac{\sum_{i=1}^N w_i^{(m)} \mathbb{I}(y_i \neq h_m(\mathbf{x}_i))}{\sum_{i=1}^N w_i^{(m)}} \implies \sum_{i=1}^N w_i^{(m)} \mathbb{I}(y_i \neq h_m(\mathbf{x}_i)) = \epsilon_m \sum_{i=1}^N w_i^{(m)}$$

Substituting this back into the loss expression:
$$\mathcal{L} = \sum_{i=1}^N w_i^{(m)} \left[ e^{-\beta_m}(1 - \epsilon_m) + e^{\beta_m} \epsilon_m \right]$$

To find the optimal step size $\beta_m$, we differentiate $\mathcal{L}$ with respect to $\beta_m$ and set the derivative to zero:
$$\frac{\partial \mathcal{L}}{\partial \beta_m} = \sum_{i=1}^N w_i^{(m)} \left[ -e^{-\beta_m}(1 - \epsilon_m) + e^{\beta_m} \epsilon_m \right] = 0$$

Divide the entire equation by the positive constant term $\sum_{i=1}^N w_i^{(m)}$:
$$-e^{-\beta_m}(1 - \epsilon_m) + e^{\beta_m} \epsilon_m = 0$$
$$e^{\beta_m} \epsilon_m = e^{-\beta_m}(1 - \epsilon_m)$$

Multiply both sides by $e^{\beta_m}$:
$$e^{2\beta_m} \epsilon_m = 1 - \epsilon_m \implies e^{2\beta_m} = \frac{1 - \epsilon_m}{\epsilon_m}$$

Taking the natural logarithm and solving for $\beta_m$:
$$\beta_m = \frac{1}{2} \log\left( \frac{1 - \epsilon_m}{\epsilon_m} \right)$$

---

## Q2: Show how XGBoost utilizes a second-order Taylor expansion of the loss function to derive the optimal leaf weight $w_j^*$ and split gain equation.

### Standard Answer
At iteration $t$, we add regression tree $f_t$ to minimize the regularized loss:
$$\mathcal{L}^{(t)} = \sum_{i=1}^N \mathcal{L}(y_i, F_{t-1}(\mathbf{x}_i) + f_t(\mathbf{x}_i)) + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2$$

Approximating the loss using the second-order Taylor expansion around $F_{t-1}(\mathbf{x}_i)$:
$$\mathcal{L}^{(t)} \approx \sum_{i=1}^N \left[ \mathcal{L}(y_i, F_{t-1}(\mathbf{x}_i)) + g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2$$
where $g_i$ and $h_i$ are the first and second-order derivatives of the loss with respect to the active predictions.

Remove the constant term $\mathcal{L}(y_i, F_{t-1}(\mathbf{x}_i))$ and group the sum over terminal leaf nodes $j = 1, \dots, T$:
$$\tilde{\mathcal{L}}^{(t)} = \sum_{j=1}^T \left[ \left( \sum_{i \in I_j} g_i \right) w_j + \\frac{1}{2} \left( \sum_{i \in I_j} h_i + \\lambda \right) w_j^2 \\right] + \\gamma T$$
Let $G_j = \\sum_{i \\in I_j} g_i$ and $H_j = \\sum_{i \\in I_j} h_i$:
$$\\tilde{\\mathcal{L}}^{(t)} = \\sum_{j=1}^T \\left[ G_j w_j + \\frac{1}{2} (H_j + \\lambda) w_j^2 \\right] + \\gamma T$$

**1. Deriving Optimal Leaf Weight $w_j^*$:**
Since the leaves are independent, we solve for each $w_j$ by differentiating the objective and setting to zero:
$$\\frac{\\partial \\tilde{\\mathcal{L}}^{(t)}}{\\partial w_j} = G_j + (H_j + \\lambda) w_j = 0 \\implies w_j^* = -\\frac{G_j}{H_j + \\lambda}$$

**2. Deriving Structure Score (Optimal Objective):**
Substitute $w_j^*$ back into the objective:
$$\\tilde{\\mathcal{L}}^{(t)}(q) = \\sum_{j=1}^T \\left[ G_j \\left( -\\frac{G_j}{H_j + \\lambda} \\right) + \\frac{1}{2} (H_j + \\lambda) \\left( -\\frac{G_j}{H_j + \\lambda} \\right)^2 \\right] + \\gamma T = -\\frac{1}{2} \\sum_{j=1}^T \\frac{G_j^2}{H_j + \\lambda} + \\gamma T$$

**3. Deriving Split Gain Equation:**
The gain of partitioning parent $P$ into left child $L$ and right child $R$ is the reduction in cost (reduction in negative score):
$$\\text{Gain} = \\tilde{\\mathcal{L}}^{(t)}_P - \\left( \\tilde{\\mathcal{L}}^{(t)}_L + \\tilde{\\mathcal{L}}^{(t)}_R \\right) = \\frac{1}{2} \\left[ \\frac{G_L^2}{H_L + \\lambda} + \\frac{G_R^2}{H_R + \\lambda} - \\frac{G_P^2}{H_P + \\lambda} \\right] - \\gamma$$

---

## Q3: Contrast LightGBM and CatBoost. Discuss how they handle tree growth and data sampling, and specify the production scenarios where each library is preferred.

### Standard Answer
*   **LightGBM (Leaf-Wise & Histograms):**
    *   **Tree Growth:** Leaf-wise growth. It splits the leaf node that yields the largest loss reduction, producing deep, highly asymmetric trees. This minimizes loss faster but can overfit on small datasets.
    *   **Data Processing:** Uses histogram-based binning (discretizing continuous features to 256 bins), reducing split-search complexity. It employs GOSS (Gradient-based One-Side Sampling) to drop samples with small gradients, focusing strictly on high-error instances.
    *   **Scenario:** Preferred for large-scale, high-dimensional tabular datasets (e.g. ad click prediction, web search ranking) where sub-minute training speeds and low memory consumption are critical.
*   **CatBoost (Symmetric Oblivious Trees & Ordered Boosting):**
    *   **Tree Growth:** Level-wise symmetric growth. It applies the identical split condition across all nodes at a given level. The resulting symmetric trees are highly regularized, preventing overfitting and enabling fast inference via bitwise index mapping.
    *   **Data Processing:** Employs Ordered Boosting to eliminate target leakage (prediction shift) by computing gradients on out-of-history permutations of the training set. It implements a robust, smoothed symmetric target encoding for categorical features during split evaluations.
    *   **Scenario:** Preferred for tabular datasets containing many high-cardinality categorical features (e.g. e-commerce search, recommendation engines, user demographics) where standard encoders lead to overfitting.
