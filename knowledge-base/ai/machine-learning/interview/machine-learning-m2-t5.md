# Ascendrite Interview Prep: Production Feature Engineering

## Q1: Why does L1 regularization (LASSO) yield sparse parameter weights, whereas L2 regularization (Ridge) only shrinks them close to zero?

### Standard Answer
Geometrically, the constraint region for L1 regularization is defined by the L1 norm:
$$\|\boldsymbol{\beta}\|_1 \le t$$
In a two-dimensional parameter space, this constraint boundary forms a diamond shape with sharp corners located directly on the coordinate axes.

The constraint region for L2 regularization is defined by the L2 norm:
$$\|\boldsymbol{\beta}\|_2^2 \le t$$
This constraint boundary forms a circle.

The optimal parameters occur where the contours of the primary loss function intersect the constraint region. For L1, the contours of the loss function are highly likely to touch the sharp corners of the diamond first. When an intersection occurs at a corner, the parameter weight for the other dimension is set to exactly zero. For L2, the circular boundary has no corners, so the contours intersect at arbitrary non-zero points along the curve, shrinking parameters but rarely setting them to exactly zero.

---

## Q2: You are asked to target encode a category feature. What is Laplace smoothing, and how does it prevent overfitting?

### Standard Answer
Direct target encoding replaces each category with the average target value of that category in the training set. If a category occurs very rarely (e.g., only once), this creates a highly volatile estimate that leads to overfitting.

Laplace smoothing stabilizes the encoding by taking a weighted average of the category target mean and the global target mean:
$$S_i = \lambda(n_i) \bar{y}_i + (1 - \lambda(n_i)) \mu_y$$
where $\lambda(n_i) = \frac{n_i}{n_i + m}$ and $m$ is the smoothing weight.

If a category has a high sample size ($n_i \gg m$), the weight $\lambda(n_i) \to 1$, allowing the model to use the category's empirical mean. If a category is rare ($n_i \approx 0$), the weight $\lambda(n_i) \to 0$, pulling the value toward the global average, regularizing the feature.

---

## Q3: Can you use t-SNE in an online prediction pipeline to reduce input dimension from 100 features to 2?

### Standard Answer
No. t-SNE is a non-linear visualization algorithm that does not learn a projection function or parametric mapping matrix. It optimizes the low-dimensional embeddings directly for a specific batch of data. You cannot transform new, unseen test observations using a pre-fit t-SNE model. For online feature pipelines, you must use parametric projection methods like PCA or UMAP, which support projecting new samples.
