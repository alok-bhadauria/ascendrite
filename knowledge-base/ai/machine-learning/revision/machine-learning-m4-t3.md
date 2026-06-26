# Ascendrite Revision Layer: Decision Trees Mathematics

## 1. Impurity Metrics (Binary case: $p$ is class 1 ratio)

### Gini Impurity (Expected misclassification rate)
$$H_{\text{Gini}}(Q_m) = 1 - \sum_{k=1}^K p_{mk}^2$$
*   *Binary scale:* $p \in [0, 1] \implies H_{\text{Gini}}(p) \in [0, 0.5]$. Peak value is $0.5$ at $p=0.5$.

### Shannon Entropy (Average information surprise)
$$H_{\text{Ent}}(Q_m) = -\sum_{k=1}^K p_{mk} \log_2(p_{mk})$$
*   *Binary scale:* $p \in [0, 1] \implies H_{\text{Ent}}(p) \in [0, 1.0]$. Peak value is $1.0$ at $p=0.5$.

---

## 2. Split Selection Criteria

### Information Gain (Classification)
$$\text{IG}(Q_m, S) = H(Q_m) - \frac{|Q_L|}{|Q_m|} H(Q_L) - \frac{|Q_R|}{|Q_m|} H(Q_R)$$

### Variance Reduction (Regression)
$$H_{\text{Var}}(Q_m) = \frac{1}{|Q_m|} \sum_{i \in Q_m} (y_i - \bar{y}_m)^2$$
$$\text{VR}(Q_m, S) = H_{\text{Var}}(Q_m) - \left( \frac{|Q_L|}{|Q_m|} H_{\text{Var}}(Q_L) + \frac{|Q_R|}{|Q_m|} H_{\text{Var}}(Q_R) \right)$$
*   *Prediction:* Regression leaf predicts constant mean $\bar{y}$ of samples in that partition.

---

## 3. Cost-Complexity Pruning (Post-Pruning)

Balances tree training impurity $R(T)$ and terminal leaf counts $|T|$:
$$R_\alpha(T) = R(T) + \alpha |T|$$

### Weakest-Link Algorithm
To prune a branch $T_t$ rooted at node $t$ into a single leaf node:
*   Pruning occurs when cost of keeping subtree equals cost of single leaf:
    $$R(t) + \alpha = R(T_t) + \alpha |T_t| \implies \alpha = g(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}$$
*   **$g(t)$ interpretation:** Impurity increase rate per leaf node removed.
*   **Method:** Recursively find and prune node $t$ that minimizes $g(t)$, creating a nested sequence of candidate subtrees. Select optimal subtree via cross-validation.
