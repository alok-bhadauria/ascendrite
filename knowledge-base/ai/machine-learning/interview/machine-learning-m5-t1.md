# Ascendrite Interview Prep: Clustering Mechanics & Convergence

## Q1: Prove that the K-Means coordinate descent algorithm (Lloyd's algorithm) is guaranteed to converge to a local minimum in a finite number of iterations.

### Standard Answer
The K-Means optimization objective is the Within-Cluster Sum of Squares (WCSS):
$$J(\mathcal{C}, \boldsymbol{\mu}) = \sum_{j=1}^k \sum_{\mathbf{x}_i \in C_j} \|\mathbf{x}_i - \boldsymbol{\mu}_j\|_2^2$$
where $\mathcal{C}$ represents cluster assignments and $\boldsymbol{\mu}$ represents centroids. Lloyd's algorithm optimizes $J$ by alternating updates of $\mathcal{C}$ and $\boldsymbol{\mu}$.

1.  **Monotonic Descent during Assignment:**
    In the assignment step, we hold centroids $\boldsymbol{\mu}_j^{(t)}$ constant and find the new partition $\mathcal{C}^{(t+1)}$. For each sample $\mathbf{x}_i$:
    $$c_i^{(t+1)} = \operatorname{argmin}_{j} \|\mathbf{x}_i - \boldsymbol{\mu}_j^{(t)}\|_2^2$$
    Since each point is mapped to its closest centroid, the sum of squared distances must decrease or remain constant:
    $$J(\mathcal{C}^{(t+1)}, \boldsymbol{\mu}^{(t)}) \le J(\mathcal{C}^{(t)}, \boldsymbol{\mu}^{(t)})$$
2.  **Monotonic Descent during Centroid Update:**
    In the update step, we hold assignments $\mathcal{C}^{(t+1)}$ constant and compute new centroids $\boldsymbol{\mu}_j^{(t+1)}$. For each cluster $C_j$:
    $$\boldsymbol{\mu}_j^{(t+1)} = \operatorname{argmin}_{\mathbf{u}} \sum_{\mathbf{x}_i \in C_j} \|\mathbf{x}_i - \mathbf{u}\|_2^2$$
    Differentiating and setting to zero yields the arithmetic mean $\boldsymbol{\mu}_j^{(t+1)} = \frac{1}{|C_j|} \sum_{\mathbf{x}_i \in C_j} \mathbf{x}_i$. Since the mean mathematically minimizes the sum of squared distances for any set of vectors, this update must decrease or keep the objective constant:
    $$J(\mathcal{C}^{(t+1)}, \boldsymbol{\mu}^{(t+1)}) \le J(\mathcal{C}^{(t+1)}, \boldsymbol{\mu}^{(t)})$$
3.  **Finiteness and Convergence:**
    Combining both steps shows that the objective decreases monotonically:
    $$J(\mathcal{C}^{(t+1)}, \boldsymbol{\mu}^{(t+1)}) \le J(\mathcal{C}^{(t)}, \boldsymbol{\mu}^{(t)})$$
    Since $J \ge 0$, the sequence of objectives must converge.
    Furthermore, the number of distinct ways to partition $N$ samples into $k$ clusters is $k^N$, which is finite. Because $J$ decreases strictly at each step where the partition changes, the algorithm cannot visit the same partition twice. Therefore, the coordinate descent must terminate at a local minimum in a finite number of iterations.

---

## Q2: Outline the K-Means++ initialization algorithm. Why does it improve upon standard random initialization?

### Standard Answer
*   **The Algorithm:**
    1.  Select the first centroid $\boldsymbol{\mu}_1$ uniformly at random from the dataset $X$.
    2.  For each remaining point $\mathbf{x}_i \in X$, compute the distance $D(\mathbf{x}_i)$ to the nearest already chosen centroid:
        $$D(\mathbf{x}_i) = \min_{p \in \{1,\dots,j-1\}} \|\mathbf{x}_i - \boldsymbol{\mu}_p\|_2$$
    3.  Select the next centroid $\boldsymbol{\mu}_j$ randomly from $X$ with probability proportional to the squared distance:
        $$P(\mathbf{x}_i) = \frac{D(\mathbf{x}_i)^2}{\sum_{l=1}^N D(\mathbf{x}_l)^2}$$
    4.  Repeat steps 2 and 3 until $k$ centroids are chosen.

*   **Why it Prevents Failures:**
    Standard random initialization (Forgy method) frequently selects initial centroids that lie close to each other. When centroids are grouped inside a single high-density cluster, K-Means is forced to split that single natural cluster while merging other distant, distinct clusters. This locks the model in a poor local minimum.
    K-Means++ addresses this by selecting centroids sequentially using a distance-weighted probability distribution ($D^2$ weighting). Points that lie far from existing centroids have high $D(\mathbf{x}_i)^2$ values, making them highly likely to be selected as new centroids, while points close to existing centroids are ignored. This guarantees that initial centroids are distributed across the dataset, yielding an expected approximation ratio of $\mathcal{O}(\log k)$ relative to the global WCSS minimum.

---

## Q3: Formulate and compare the density connectivity rules of DBSCAN. How do they enable the isolation of non-convex clusters?

### Standard Answer
DBSCAN defines clusters based on local density within a search radius $\epsilon$ containing at least $\text{MinPts}$ samples.

*   **1. Directly Density-Reachable:**
    A point $\mathbf{q}$ is directly density-reachable from $\mathbf{p}$ if:
    *   $\mathbf{q}$ lies in the $\epsilon$-neighborhood of $\mathbf{p}$: $\|\mathbf{q} - \mathbf{p}\|_2 \le \epsilon$.
    *   $\mathbf{p}$ is a core point: $|N_{\epsilon}(\mathbf{p})| \ge \text{MinPts}$.
    This relationship is asymmetric: a border point can be reachable from a core point, but a core point is not reachable from a border point.
*   **2. Density-Reachable:**
    A point $\mathbf{q}$ is density-reachable from $\mathbf{p}$ if there exists a chain of points $\mathbf{p}_1, \dots, \mathbf{p}_n$ where $\mathbf{p}_1 = \mathbf{p}$, $\mathbf{p}_n = \mathbf{q}$, and each $\mathbf{p}_{i+1}$ is directly density-reachable from $\mathbf{p}_i$. This represents the transitive propagation of density reachability.
*   **3. Density-Connected:**
    Two points $\mathbf{p}$ and $\mathbf{q}$ are density-connected if there exists a core point $\mathbf{o}$ such that both $\mathbf{p}$ and $\mathbf{q}$ are density-reachable from $\mathbf{o}$. This is a symmetric relationship.

**Isolating Non-Convex Clusters:**
K-Means assumes convex Voronoi partitions because it maps points to the single closest centroid, which cannot model nested rings or hollow structures.
DBSCAN does not rely on centroids. Instead, it groups points that are density-connected. As long as a continuous path of high-density nodes (core points within $\epsilon$ distance) exists, the cluster can expand along arbitrary non-convex geometries (like curves or spirals), while sparse regions are correctly discarded as noise.
