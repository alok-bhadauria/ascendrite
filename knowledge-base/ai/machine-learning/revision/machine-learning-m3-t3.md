# Ascendrite Revision Layer: KNN & Naive Bayes Algorithms

## 1. KNN Distance Metrics & Curse of Dimensionality

### Minkowski Distance
General distance formulation:
$$D_p(\mathbf{x}_a, \mathbf{x}_b) = \left( \sum_{i=1}^d |x_{a,i} - x_{b,i}|^p \right)^{1/p}$$
*   $p=1$: Manhattan distance ($L_1$ norm).
*   $p=2$: Euclidean distance ($L_2$ norm).

### Curse of Dimensionality
As feature dimension $d \to \infty$, the volume of the space increases exponentially. Data points become nearly equidistant, rendering nearest neighbor search ineffective:
$$\lim_{d \to \infty} \frac{D_{\max} - D_{\min}}{D_{\min}} = 0$$

---

## 2. Spatial Indexing Acceleration

*   **KD-Tree:** Axis-aligned hyperplane splits using feature medians. Best for low dimensions ($d < 20$). In high dimensions, query search degrades to $\mathcal{O}(N \cdot d)$ due to extensive back-tracking.
*   **Ball-Tree:** Nesting hypersphere (ball) partitions. Efficient pruning in high dimensions based on centroid distances and radii.

---

## 3. Naive Bayes & Laplace Smoothing

### Conditional Independence Assumption
Assumes features are independent of each other given the class label:
$$P(\mathbf{x} \mid Y = c_k) = \prod_{i=1}^d P(x_i \mid Y = c_k)$$

### Laplace Smoothing
Prevents zero-probability errors by regularizing counts:
$$\hat{P}(x_i = v_j \mid Y = c_k) = \frac{N_{k,j} + \alpha}{N_k + \alpha \cdot V_i}$$
where $\alpha$ is the smoothing parameter and $V_i$ is the vocabulary/unique category size of feature $x_i$.
