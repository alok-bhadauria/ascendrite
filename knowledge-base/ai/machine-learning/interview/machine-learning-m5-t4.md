# Ascendrite Interview Prep: Explainable AI (XAI) Mathematics

## Q1: Explain how the Shapley value formulation from cooperative game theory distributes feature attributions, and show mathematically how it satisfies the Efficiency and Dummy (Null Player) axioms.

### Standard Answer
The **Shapley value** calculates the unique, fair attribution $\phi_i(v)$ for each feature $i$ in a feature set $F$ given a characteristic function $v(S)$ representing the prediction of the model using a subset of features $S \subseteq F$:

$$\phi_i(v) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} \left[ v(S \cup \{i\}) - v(S) \right]$$

The term $\left[ v(S \cup \{i\}) - v(S) \right]$ is the marginal contribution of feature $i$ when added to coalition $S$. The weight $\frac{|S|! (|F| - |S| - 1)!}{|F|!}$ represents the probability that feature $i$ enters coalition $S$ under a uniform permutation of all features in $F$.

#### 1. Proof of the Efficiency Axiom
The Efficiency axiom states that the sum of all feature attributions equals the total gain:
$$\sum_{i \in F} \phi_i(v) = v(F) - v(\emptyset)$$

Let $R$ be a random permutation of features, and let $S_i^R$ be the set of features appearing before feature $i$ in $R$. The marginal contribution of feature $i$ in permutation $R$ is $v(S_i^R \cup \{i\}) - v(S_i^R)$. Since the sum of marginal contributions along any permutation sequence forms a telescoping sum:
$$\sum_{i \in F} \left[ v(S_i^R \cup \{i\}) - v(S_i^R) \right] = v(F) - v(\emptyset)$$

By definition, the Shapley value $\phi_i(v)$ is the expected marginal contribution of feature $i$ averaged over all possible permutations $R$:
$$\phi_i(v) = \frac{1}{|F|!} \sum_{R} \left[ v(S_i^R \cup \{i\}) - v(S_i^R) \right]$$

Summing over all $i$:
$$\sum_{i \in F} \phi_i(v) = \sum_{i \in F} \left( \frac{1}{|F|!} \sum_{R} \left[ v(S_i^R \cup \{i\}) - v(S_i^R) \right] \right) = \frac{1}{|F|!} \sum_{R} \left( \sum_{i \in F} \left[ v(S_i^R \cup \{i\}) - v(S_i^R) \right] \right)$$
$$\sum_{i \in F} \phi_i(v) = \frac{1}{|F|!} \sum_{R} (v(F) - v(\emptyset)) = \frac{|F|!}{|F|!} (v(F) - v(\emptyset)) = v(F) - v(\emptyset)$$
This completes the proof of Efficiency.

#### 2. Proof of the Dummy (Null Player) Axiom
The Dummy axiom states that if feature $i$ makes zero marginal contribution to all coalitions, its attribution is zero:
$$\text{If } v(S \cup \{i\}) = v(S) \quad \forall S \subseteq F \setminus \{i\}, \quad \text{then } \phi_i(v) = 0$$

If $v(S \cup \{i\}) - v(S) = 0$ for all $S \subseteq F \setminus \{i\}$, then every term in the Shapley summation is zero:
$$\phi_i(v) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} (0) = 0$$
This completes the proof of the Dummy axiom.

---

## Q2: Deriving KernelSHAP: How does it frame the computation of Shapley values as a weighted linear regression, and how does the SHAP Kernel enforce the game-theoretic axioms?

### Standard Answer
Rather than evaluating the exponential number of coalitions directly, **KernelSHAP** treats Shapley values as coefficients of a local linear surrogate model $g(z') = \phi_0 + \sum_{i=1}^M \phi_i z'_i$, where $z' \in \{0, 1\}^M$ is a coalition vector.

#### 1. The Regression Objective
KernelSHAP minimizes the weighted squared loss:
$$\min_{\phi_0, \dots, \phi_M} \sum_{z' \in Z'} \left[ f(h_{\mathbf{x}}(z')) - \left( \phi_0 + \sum_{i=1}^M \phi_i z'_i \right) \right]^2 \pi_{\mathbf{x}}(z')$$

#### 2. The SHAP Kernel
The regression weights are assigned via the SHAP Kernel:
$$\pi_{\mathbf{x}}(z') = \frac{M - 1}{\binom{M}{|z'|} |z'| (M - |z'|)}$$

#### 3. How the Kernel Enforces Axioms
The denominator contains the term $|z'| (M - |z'|)$. 
*   When $|z'| = 0$ (empty coalition) or $|z'| = M$ (full coalition), the kernel weight $\pi_{\mathbf{x}}(z')$ becomes infinite:
    $$\lim_{|z'| \to 0} \pi_{\mathbf{x}}(z') = \infty \quad \text{and} \quad \lim_{|z'| \to M} \pi_{\mathbf{x}}(z') = \infty$$
*   These infinite weights function as hard constraints in the weighted least-squares optimization. The optimizer is forced to set the prediction error to zero for these two coalitions:
    1.  For $z' = \mathbf{0}$ (where $|z'|=0$): $g(\mathbf{0}) = \phi_0 = f(h_{\mathbf{x}}(\mathbf{0})) = v(\emptyset)$.
    2.  For $z' = \mathbf{1}$ (where $|z'|=M$): $g(\mathbf{1}) = \phi_0 + \sum_{i=1}^M \phi_i = f(h_{\mathbf{x}}(\mathbf{1})) = v(F)$.
*   Substituting $\phi_0 = v(\emptyset)$ into the second equation yields:
    $$\sum_{i=1}^M \phi_i = v(F) - v(\emptyset)$$
    which is the **Efficiency** axiom.
*   By setting the regression weights to match the marginal probability weights of cooperative game theory, the coefficients $\phi_i$ are mathematically equivalent to the exact Shapley values, thereby satisfying all four game-theoretic axioms.

---

## Q3: Contrast LIME and KernelSHAP. What are the key mathematical differences in their objectives, and why does LIME violate the consistency axiom?

### Standard Answer
While both LIME and KernelSHAP construct local linear models $g(z') = \mathbf{w}^{\top} z'$ to approximate a black-box model $f$, they differ fundamentally in their optimization objectives and kernels.

#### 1. Comparison of Optimization Frameworks
*   **Objective Functions:**
    *   **LIME:** Minimizes a local loss with a complexity penalty:
        $$\operatorname{argmin}_{g \in G} \sum_{z, z' \in Z} \pi_{\mathbf{x}}(z) \left( f(z) - g(z') \right)^2 + \Omega(g)$$
        where $\pi_{\mathbf{x}}(z)$ is an exponential similarity kernel based on distance in the feature space:
        $$\pi_{\mathbf{x}}(z) = \exp\left( -\frac{D(\mathbf{x}, z)^2}{\sigma^2} \right)$$
    *   **KernelSHAP:** Minimizes a weighted squared loss without a complexity penalty during the main regression, enforcing local constraints through the game-theoretic SHAP kernel:
        $$\operatorname{argmin}_{g \in G} \sum_{z' \in Z'} \left[ f(h_{\mathbf{x}}(z')) - g(z') \right]^2 \pi_{\mathbf{x}}(z')$$
        where $\pi_{\mathbf{x}}(z')$ is determined by the size of the feature coalition, independent of the distance between actual feature values.

#### 2. Why LIME Violates the Consistency Axiom
The **Consistency (Monotonicity)** axiom states that if a model changes such that the marginal contribution of a feature increases or stays the same for all coalitions, its attribution must not decrease.

*   LIME uses a heuristic distance-based exponential kernel $\pi_{\mathbf{x}}(z)$. This means that the weight of a perturbed sample is dependent on the neighborhood distance parameter $\sigma$ and distance metric $D(\mathbf{x}, z)$.
*   Because LIME's sample weights depend on distance, the local linear surrogate is fitting the model's output weighted by spatial proximity. If a model's local behavior changes, the relative attributions can shift unpredictably based on how perturbations are distributed in the input space.
*   Consequently, a feature can become globally more important in the black-box model, but its LIME attribution can decrease because the local density weights shift, violating the consistency axiom. KernelSHAP's weights depend solely on the coalition structure, which guarantees consistency.
