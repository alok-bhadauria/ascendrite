# Ascendrite Interview Prep: KNN & Naive Bayes Algorithms

## Q1: Explain the 'Curse of Dimensionality' geometrically and its direct impact on K-Nearest Neighbors.

### Standard Answer
The **Curse of Dimensionality** refers to the exponential volume expansion of a coordinate space as the feature dimension $d$ increases.

Geometrically, consider a $d$-dimensional unit hypercube. The volume of a smaller concentric hypercube of edge length $1 - 2\epsilon$ is $(1 - 2\epsilon)^d$. As $d \to \infty$, this volume approaches 0. This means that almost all of the volume of a hypercube is located near its outer shell.

For KNN, this sparsity means that as dimensions increase:
1.  All data points migrate to the outer boundaries of the coordinate space, leaving the center empty.
2.  The distances between any two points converge. The difference between the distance to the nearest neighbor ($D_{\min}$) and the furthest neighbor ($D_{\max}$) approaches zero relative to $D_{\min}$:
    $$\lim_{d \to \infty} \frac{D_{\max} - D_{\min}}{D_{\min}} = 0$$
Because all points become nearly equidistant, the concept of 'closeness' is lost, causing KNN to fail in high-dimensional settings unless dimensionality reduction (like PCA) is performed first.

---

## Q2: Contrast KD-Trees and Ball-Trees. Under what conditions does KD-Tree performance degrade to a naive search?

### Standard Answer
*   **KD-Tree:** Recurrently splits the space along axis-aligned hyperplanes at the median value of a single feature dimension.
*   **Ball-Tree:** Recursively partitions data using nested hyperspheres defined by centroids and radii.

**KD-Tree Performance Degradation:**
In low-dimensional spaces ($d < 10$), KD-Tree queries run in $\mathcal{O}(\log N \cdot d)$ time. However, as the dimension $d$ increases ($d > 20$), the query point lies close to many splitting hyperplanes. This forces the search path to backtrack through almost all branches of the tree, rendering pruning ineffective. The computational complexity degrades back to the naive $\mathcal{O}(N \cdot d)$ linear scan. Ball-Trees mitigate this by using spherical boundaries, which prune high-dimensional spaces more effectively.

---

## Q3: What is the Naive Bayes 'conditional independence assumption,' and why do we apply Laplace smoothing?

### Standard Answer
*   **Conditional Independence Assumption:** We assume that the value of any feature $x_i$ is independent of any other feature $x_j$ ($i \neq j$) given the class label $Y$. This allows us to decompose the joint conditional probability into a product of marginals:
    $$P(x_1, \dots, x_d \mid Y) = \prod_{i=1}^d P(x_i \mid Y)$$
    This assumption is 'naive' because in real datasets, features are often correlated.
*   **Laplace Smoothing:** If a feature value $x_i = v_j$ never occurs with class $c_k$ in the training set, the probability estimate is $P(x_i = v_j \mid Y=c_k) = 0$. Since we multiply feature probabilities together, this zero term makes the entire class probability zero, regardless of other strong signals. We apply Laplace smoothing to add a regularizer $\alpha$ to the counts:
    $$\hat{P}(x_i = v_j \mid Y = c_k) = \frac{N_{k,j} + \alpha}{N_k + \alpha \cdot V_i}$$
    This guarantees non-zero probabilities for all unobserved feature values.
