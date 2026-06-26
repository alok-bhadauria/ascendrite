# Ascendrite Interview Prep: Decision Trees Mathematics

## Q1: Mathematically compare Gini Impurity and Shannon Entropy for binary classification. Why is Gini Impurity generally preferred in production tree implementations?

### Standard Answer
Let $p \in [0, 1]$ be the proportion of the positive class in a node. For binary classification ($K=2$):
1.  **Gini Impurity:**
    $$H_{\text{Gini}}(p) = 1 - \sum_{k=1}^2 p_k^2 = 1 - (p^2 + (1-p)^2) = 1 - (p^2 + 1 - 2p + p^2) = 2p(1-p)$$
    *   **Scale:** $H_{\text{Gini}}(p) \in [0, 0.5]$. Peak value is $0.5$ at $p=0.5$.
2.  **Shannon Entropy:**
    $$H_{\text{Ent}}(p) = -\sum_{k=1}^2 p_k \log_2(p_k) = -p \log_2(p) - (1-p) \log_2(1-p)$$
    *   **Scale:** $H_{\text{Ent}}(p) \in [0, 1.0]$. Peak value is $1.0$ at $p=0.5$.

**Comparison and Production Choice:**
Both metrics are smooth, symmetric, and concave functions. They reach their maximum at $p=0.5$ and vanish to $0$ at $p=0$ and $p=1$. During tree construction, they yield nearly identical splitting boundaries.
However, **Gini Impurity is preferred in production** (e.g., as the default in Scikit-Learn's DecisionTreeClassifier) because of **computational efficiency**:
*   Gini only requires basic arithmetic operations (multiplications and additions).
*   Entropy requires calculating natural or base-2 logarithms ($\log_2(p)$). Evaluating logarithmic functions requires floating-point expansions (e.g. Taylor series) inside the CPU, which is significantly slower. When scanning millions of splits over massive datasets, Gini reduces tree build times by $10\%$ to $30\%$ compared to Entropy.

---

## Q2: Detail the mechanism of Cost-Complexity Pruning (post-pruning). Derive the equation for the weakest link score $g(t)$.

### Standard Answer
Cost-Complexity Pruning minimizes a regularized objective function:
$$R_\alpha(T) = R(T) + \alpha |T|$$
where $R(T)$ is the training set impurity of the subtree $T$, $|T|$ is the number of terminal leaves, and $\alpha \ge 0$ is the regularization parameter.

**Deriving $g(t)$:**
For any internal node $t$ in a fully grown tree $T_{\text{max}}$, we consider the cost of pruning the entire subtree $T_t$ rooted at $t$ into a single leaf node $\{t\}$.
1.  If we prune $T_t$, the node $t$ becomes a leaf. The cost is:
    $$R_\alpha(\{t\}) = R(t) + \alpha \times 1 = R(t) + \alpha$$
2.  If we do not prune $T_t$, the branch remains intact. The cost is:
    $$R_\alpha(T_t) = R(T_t) + \alpha |T_t|$$

As $\alpha$ increases from $0$, the cost of keeping the subtree (which has more leaves $|T_t|$) rises faster than the cost of a single leaf. The two configurations have identical cost at a threshold value $\alpha = g(t)$:
$$R(t) + g(t) = R(T_t) + g(t) |T_t|$$
$$R(t) - R(T_t) = g(t) (|T_t| - 1)$$
$$g(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}$$

**Algorithm Execution:**
*   **Physical Meaning:** $g(t)$ represents the rate of increase in training impurity per leaf node eliminated. A small $g(t)$ indicates that the subtree $T_t$ contributes very little to training error reduction relative to its complexity.
*   **Pruning step:** The algorithm calculates $g(t)$ for all internal nodes. The node $t^*$ that minimizes $g(t)$ (the 'weakest link') is collapsed first. This process is applied recursively to construct a sequence of nested subtrees $\{T_{\text{max}} \supset T_1 \supset T_2 \supset \dots \supset t_{\text{root}}\}$. The optimal subtree is selected via cross-validation.

---

## Q3: What is the Mean Decrease in Impurity (MDI) feature importance metric, and what is its primary mathematical bias?

### Standard Answer
*   **Mechanism:**
    Mean Decrease in Impurity (MDI) measures feature importance by summing the impurity decreases (Information Gain or Gini Gain) across all nodes $t$ where a split was made on feature $X_j$, weighted by the fraction of training samples that reached those nodes:
    $$\text{MDI}(X_j) = \sum_{t \in T : \text{split}(t) = X_j} \frac{|Q_t|}{|Q|} \text{IG}(Q_t, S_t)$$
*   **Mathematical Bias:**
    MDI exhibits a severe bias toward **continuous features** or **high-cardinality categorical features** (features with many unique values).
    Because a high-cardinality feature offers many candidate split thresholds $t$, the greedy split-selection algorithm has many more opportunities to find a split that reduces Gini impurity by chance on the training set, even if the feature contains pure random noise. This causes MDI to overestimate the importance of continuous/high-cardinality features.
*   **Resolution:**
    To resolve this bias, implement **Permutation Feature Importance** evaluated on a held-out validation or test set. This evaluates the decrease in validation score when a feature's values are randomly shuffled, neutralizing the impact of training-set cardinality advantages.
