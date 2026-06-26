# Ascendrite Revision Layer: Clustering Mechanics & Convergence

## 1. K-Means & K-Means++

### Optimization Objective (WCSS)
$$J(\mathcal{C}, \boldsymbol{\mu}) = \sum_{j=1}^k \sum_{\mathbf{x}_i \in C_j} \|\mathbf{x}_i - \boldsymbol{\mu}_j\|_2^2$$
Optimized via Lloyd's Coordinate Descent:
*   **Assignment Step:** Set $c_i^{(t)} = \operatorname{argmin}_{j} \|\mathbf{x}_i - \boldsymbol{\mu}_j^{(t)}\|_2^2$ (minimizes $J$ w.r.t assignments).
*   **Update Step:** Set $\boldsymbol{\mu}_j^{(t+1)} = \frac{1}{|C_j|} \sum_{\mathbf{x}_i \in C_j} \mathbf{x}_i$ (minimizes $J$ w.r.t centroids).
*   *Convergence:* $J$ decreases monotonically and partitions are finite, guaranteeing convergence to a local minimum in finite steps.

### K-Means++ Initialization
1.  Choose first centroid $\boldsymbol{\mu}_1$ uniformly at random.
2.  Choose next centroid $\boldsymbol{\mu}_j$ randomly with probability:
    $$P(\mathbf{x}_i) = \frac{D(\mathbf{x}_i)^2}{\sum_{l=1}^N D(\mathbf{x}_l)^2}$$
    where $D(\mathbf{x}_i)$ is distance to nearest active centroid. Yields an expected $\mathcal{O}(\log k)$ approximation ratio.

---

## 2. DBSCAN & Silhouette Score

### DBSCAN Density Rules
Requires radius $\epsilon > 0$ and $\text{MinPts} \ge 1$. $N_{\epsilon}(\mathbf{x}) = \{\mathbf{z} \in X \mid \|\mathbf{x} - \mathbf{z}\|_2 \le \epsilon\}$.
*   **Core Point:** $|N_{\epsilon}(\mathbf{x})| \ge \text{MinPts}$.
*   **Border Point:** $|N_{\epsilon}(\mathbf{x})| < \text{MinPts}$, but lies in $\epsilon$-neighborhood of a core point.
*   **Noise Point:** Neither core nor border.
*   **Directly Density-Reachable:** $\mathbf{q} \in N_{\epsilon}(\mathbf{p})$ where $\mathbf{p}$ is a core point.
*   **Density-Connected:** $\mathbf{p}$ and $\mathbf{q}$ are density-connected if they are both density-reachable from a common core point $\mathbf{o}$.

### Silhouette Coefficient
For sample $\mathbf{x}_i \in C_A$:
$$s(\mathbf{x}_i) = \frac{b(\mathbf{x}_i) - a(\mathbf{x}_i)}{\max(a(\mathbf{x}_i), b(\mathbf{x}_i))}$$
*   $a(\mathbf{x}_i)$: mean intra-cluster distance.
*   $b(\mathbf{x}_i)$: mean distance to the nearest neighboring cluster.
*   *Range:* $s(\mathbf{x}_i) \in [-1, 1]$. Close to 1 is optimal clustering.

---

## 3. Hierarchical Linkages

*   **Single Linkage:** $d(A, B) = \min_{\mathbf{x} \in A, \mathbf{y} \in B} \|\mathbf{x} - \mathbf{y}\|_2$. Causes chaining.
*   **Complete Linkage:** $d(A, B) = \max_{\mathbf{x} \in A, \mathbf{y} \in B} \|\mathbf{x} - \mathbf{y}\|_2$. Forces compact, spherical clusters.
*   **Average Linkage:** $d(A, B) = \frac{1}{|A||B|} \sum_{\mathbf{x} \in A} \sum_{\mathbf{y} \in B} \|\mathbf{x} - \mathbf{y}\|_2$.
*   **Ward's Linkage:** Merges clusters that minimize WCSS variance increase:
    $$d(A, B) = \sqrt{\frac{|A||B|}{|A| + |B|}} \|\boldsymbol{\mu}_A - \boldsymbol{\mu}_B\|_2$$
