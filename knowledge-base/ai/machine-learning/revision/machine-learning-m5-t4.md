# Ascendrite Revision Layer: Explainable AI (XAI) Mathematics

## 1. Shapley Values & Game Theory Axioms

### Shapley Value Formulation
For a feature set $F$ and a characteristic function $v(S)$ representing the expected output of a model given a feature subset $S \subseteq F \setminus \{i\}$:

$$\phi_i(v) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} \left[ v(S \cup \{i\}) - v(S) \right]$$

*   **Interpretation:** The weighted sum of marginal contributions $v(S \cup \{i\}) - v(S)$ of feature $i$ across all coalitions $S$.
*   **Permutations:** The weight corresponds to the fraction of permutations of features where $i$ enters immediately after the coalition $S$.

### The Four Axioms
The Shapley value is the unique attribution method satisfying:
1.  **Efficiency:** The total attribution equals the difference between the full model prediction and baseline expectation:
    $$\sum_{i \in F} \phi_i(v) = v(F) - v(\emptyset)$$
2.  **Symmetry:** Equal marginal contributors receive equal attributions:
    $$\text{If } v(S \cup \{i\}) = v(S \cup \{j\}) \quad \forall S \subseteq F \setminus \{i, j\}, \quad \text{then } \phi_i(v) = \phi_j(v)$$
3.  **Dummy:** Non-contributors receive zero attribution:
    $$\text{If } v(S \cup \{i\}) = v(S) \quad \forall S \subseteq F \setminus \{i\}, \quad \text{then } \phi_i(v) = 0$$
4.  **Additivity:** For independent games $v$ and $w$, attributions add linearly:
    $$\phi_i(v + w) = \phi_i(v) + \phi_i(w)$$

---

## 2. KernelSHAP

### Local Linear Surrogate
SHAP approximates model predictions around a query sample $\mathbf{x}$ using a linear model $g(z') = \phi_0 + \sum_{i=1}^M \phi_i z'_i$, where $z' \in \{0, 1\}^M$ is a binary coalition vector representing active features.

### Weighted Regression Objective
KernelSHAP solves the weighted least-squares problem:

$$\min_{\phi_0, \dots, \phi_M} \sum_{z' \in Z'} \left[ f(h_{\mathbf{x}}(z')) - \left( \phi_0 + \sum_{i=1}^M \phi_i z'_i \right) \right]^2 \pi_{\mathbf{x}}(z')$$

### The SHAP Kernel
The weights are defined by the SHAP Kernel:

$$\pi_{\mathbf{x}}(z') = \frac{M - 1}{\binom{M}{|z'|} |z'| (M - |z'|)}$$

*   $M$: The total number of features (maximum coalition size).
*   $|z'|$: The number of active features in the coalition ($|z'| = \sum_{j=1}^M z'_j$).
*   *Property:* $\pi_{\mathbf{x}}(z') \to \infty$ as $|z'| \to 0$ or $|z'| \to M$, enforcing the Efficiency axiom.

---

## 3. LIME (Local Interpretable Model-agnostic Explanations)

### Optimization Objective
LIME solves:

$$\xi(\mathbf{x}) = \operatorname{argmin}_{g \in G} \mathcal{L}(f, g, \pi_{\mathbf{x}}) + \Omega(g)$$

*   $\mathcal{L}(f, g, \pi_{\mathbf{x}})$: Local loss of surrogate $g$ approximating black-box $f$.
*   $\Omega(g)$: Regularization term penalizing surrogate complexity (e.g., number of non-zero coefficients).

### Local Loss Formulation
$$\mathcal{L}(f, g, \pi_{\mathbf{x}}) = \sum_{z, z' \in Z} \pi_{\mathbf{x}}(z) \left( f(z) - g(z') \right)^2$$

### Similarity Kernel
The local neighborhood is defined by the distance $D(\mathbf{x}, z)$ and neighborhood width $\sigma$:

$$\pi_{\mathbf{x}}(z) = \exp\left( -\frac{D(\mathbf{x}, z)^2}{\sigma^2} \right)$$
