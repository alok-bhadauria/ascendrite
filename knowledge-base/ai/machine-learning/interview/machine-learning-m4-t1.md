# Ascendrite Interview Prep: Generalization Theory & Overfitting

## Q1: Formally derive the Bias-Variance Decomposition of expected prediction error under the Squared Error loss function.

### Standard Answer
Let the target value be $y = f(\mathbf{x}) + \epsilon$, where $\mathbb{E}[\epsilon] = 0$ and $\text{Var}(\epsilon) = \sigma^2$. The noise $\epsilon$ is independent of the training data $\mathcal{D}$. Let $\hat{f}(\mathbf{x})$ denote the model trained on $\mathcal{D}$. To evaluate performance, we take the expectation over both $\mathcal{D}$ and $\epsilon$.

First, write the expected loss at a point $\mathbf{x}$:
$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \mathbb{E}[(f(\mathbf{x}) + \epsilon - \hat{f}(\mathbf{x}))^2]$$

Subtract and add $\mathbb{E}[\hat{f}(\mathbf{x})]$ inside the term:
$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \mathbb{E}\left[ \left( (f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]) + (\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x})) + \epsilon \right)^2 \right]$$

Expanding the square $(A + B + C)^2 = A^2 + B^2 + C^2 + 2AB + 2AC + 2BC$:
$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \mathbb{E}[(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2] + \mathbb{E}[(\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x}))^2] + \mathbb{E}[\epsilon^2] + 2\mathbb{E}[(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])(\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x}))] + 2\mathbb{E}[(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])\epsilon] + 2\mathbb{E}[(\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x}))\epsilon]$$

We evaluate each expectation:
1.  **Bias Term:** Since $f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]$ is a constant w.r.t training sets, the expectation is:
    $$\mathbb{E}[(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2] = (f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2 = \text{Bias}[\hat{f}(\mathbf{x})]^2$$
2.  **Variance Term:** By definition of variance:
    $$\mathbb{E}[(\hat{f}(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2] = \text{Var}(\hat{f}(\mathbf{x}))$$
3.  **Irreducible Error:** Since $\mathbb{E}[\epsilon] = 0$:
    $$\mathbb{E}[\epsilon^2] = \text{Var}(\epsilon) = \sigma^2$$
4.  **First Cross-Product:** Since $(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])$ is constant, we factor it out:
    $$2(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]) \cdot \mathbb{E}[\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x})] = 2(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]) \cdot (\mathbb{E}[\hat{f}(\mathbf{x})] - \mathbb{E}[\hat{f}(\mathbf{x})]) = 0$$
5.  **Second & Third Cross-Products:** Since $\epsilon$ is independent of the model and training set, and $\mathbb{E}[\epsilon] = 0$:
    $$2(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])\mathbb{E}[\epsilon] = 0 \quad \text{and} \quad 2\mathbb{E}[(\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x}))]\mathbb{E}[\epsilon] = 0$$

Summing the terms yields the final decomposition:
$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \text{Bias}[\hat{f}(\mathbf{x})]^2 + \text{Var}[\hat{f}(\mathbf{x})] + \sigma^2$$

---

## Q2: Contrast VC Dimension and Rademacher Complexity. Why is Rademacher Complexity considered a more refined capacity measure for practical machine learning datasets?

### Standard Answer
*   **VC Dimension:**
    *   **Definition:** The maximum size of a dataset that can be shattered (all labeling combinations realized) by the hypothesis class.
    *   **Property:** It is a static, purely combinatorial metric. It represents a worst-case capacity because it requires only *one* set of size $d$ to be shattered, ignoring the actual data distribution.
*   **Rademacher Complexity:**
    *   **Definition:** Measures the expectation of the maximum correlation between hypotheses in class $\mathcal{H}$ and random labels $\sigma_i \in \{-1, 1\}$:
        $$\hat{\mathcal{R}}_S(\mathcal{H}) = \mathbb{E}_{\boldsymbol{\sigma}} \left[ \sup_{h \in \mathcal{H}} \frac{1}{N} \sum_{i=1}^N \sigma_i h(\mathbf{x}_i) \right]$$
    *   **Property:** It is a data-dependent metric. It evaluates the model class capacity *specifically* on the empirical sample distribution $S$.

**Why Rademacher is Preferred in Practice:**
VC bounds are distribution-free, which makes them extremely loose (often pessimistic) for real-world distributions. For example, if a dataset is constrained to a narrow linear manifold, a high-parameter neural network will not express its full capacity. VC bounds cannot capture this and will predict massive overfitting. In contrast, Rademacher complexity evaluates how well the hypotheses fit noise *on the actual coordinates* of the dataset $S$. If the data coordinates are highly structured or restricted, the Rademacher complexity drops, providing much tighter and more realistic generalization bounds.

---

## Q3: Prove that linear classifiers in $\mathbb{R}^2$ have a Vapnik-Chervonenkis (VC) dimension of exactly 3.

### Standard Answer
To prove that $d_{\text{VC}}(\mathcal{H}) = 3$ for linear classifiers in $\mathbb{R}^2$, we must show two things:
1.  **Lower Bound ($\ge 3$):** There exists *at least one* set of 3 points that can be shattered.
2.  **Upper Bound ($< 4$):** *No* set of 4 points can be shattered.

**Step 1: Shattering 3 points**
Choose 3 non-collinear points forming a triangle. There are $2^3 = 8$ possible binary labelings.
*   All positives $(+, +, +)$ or all negatives $(- , -, -)$: Can be separated by placing the boundary line completely outside the triangle.
*   One positive and two negatives (e.g. $(+, -, -)$): We can draw a line separating the single positive vertex from the other two negative vertices. There are 3 such configurations.
*   Two positives and one negative (e.g. $(+, +, -)$): By symmetry, we can separate the single negative vertex from the two positive vertices.
Since all 8 labeling combinations are realizable by a straight line, this set of 3 points is shattered. Thus, $d_{\text{VC}} \ge 3$.

**Step 2: Proving 4 points cannot be shattered**
Consider any set of 4 points in $\mathbb{R}^2$. There are two possible geometric cases:
*   **Case A: The 4 points form a convex hull (quadrilateral).**
    Label the vertices in clockwise order: $A, B, C, D$. If we assign alternating labels: $A = +, B = -, C = +, D = -$, we require a line that separates $\{A, C\}$ from $\{B, D\}$. Geometrically, the line segment joining $A$ and $C$ must intersect the line segment joining $B$ and $D$. To separate the classes, a linear boundary must intersect both segments, which is impossible for a single straight line.
*   **Case B: One point lies inside the convex hull formed by the other three.**
    Let $D$ be inside the triangle formed by $A, B, C$. If we assign $A = +, B = +, C = +$ and $D = -$, any separating line must place $A, B, C$ on one side and $D$ on the other. However, the convex hull of $\{A, B, C\}$ (the triangle) contains $D$. Any half-space containing $A, B, C$ must also contain their convex hull, and thus must contain $D$. Therefore, we cannot label $D$ as negative and $A, B, C$ as positive.

Since no set of 4 points can be shattered under any configuration, $d_{\text{VC}} < 4$. Combining the steps proves that the VC dimension is exactly 3.
