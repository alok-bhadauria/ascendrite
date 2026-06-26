# Ascendrite Revision Layer: Dimensionality Reduction Derivations

## 1. PCA via Variance Maximization

Given centered dataset $\mathbf{X} \in \mathbb{R}^{N \times d}$ (mean $\boldsymbol{\mu} = \mathbf{0}$) and empirical covariance matrix $\boldsymbol{\Sigma} = \frac{1}{N} \mathbf{X}^{\top}\mathbf{X}$.
We project onto a unit direction vector $\mathbf{u}$ ($\mathbf{u}^{\top}\mathbf{u} = 1$).

### Optimization Formulation (Lagrangian)
$$\max_{\mathbf{u}} \mathbf{u}^{\top}\boldsymbol{\Sigma}\mathbf{u} \quad \text{subject to} \quad \mathbf{u}^{\top}\mathbf{u} = 1$$
$$\mathcal{L}(\mathbf{u}, \lambda) = \mathbf{u}^{\top}\boldsymbol{\Sigma}\mathbf{u} - \lambda(\mathbf{u}^{\top}\mathbf{u} - 1)$$
Setting the gradient $\nabla_{\mathbf{u}}\mathcal{L} = \mathbf{0}$ yields the Eigendecomposition:
$$\boldsymbol{\Sigma}\mathbf{u} = \lambda\mathbf{u}$$
*   **Principal Components:** Eigenvectors of $\boldsymbol{\Sigma}$.
*   **Projected Variance:** Eigenvalue $\lambda_i$.
*   *Requirement:* Mean-centering is mandatory to make the data matrix product represent covariance.

---

## 2. SVD Formulation of PCA

Operates directly on centered matrix $\mathbf{X}$ without constructing $\boldsymbol{\Sigma}$:
$$\mathbf{X} = \mathbf{U}\mathbf{S}\mathbf{V}^{\top}$$
*   **Covariance connection:**
    $$\boldsymbol{\Sigma} = \frac{1}{N} \mathbf{X}^{\top}\mathbf{X} = \frac{1}{N} \mathbf{V}\mathbf{S}^{\top}\mathbf{U}^{\top}\mathbf{U}\mathbf{S}\mathbf{V}^{\top} = \mathbf{V} \left( \frac{1}{N} \mathbf{S}^2 \right) \mathbf{V}^{\top}$$
*   **Right Singular Vectors ($\mathbf{V}$):** Identical to eigenvectors of $\boldsymbol{\Sigma}$ (principal components).
*   **Singular values ($\sigma_i$):** Related to eigenvalues by $\lambda_i = \frac{\sigma_i^2}{N}$.
*   *Advantage:* More numerically stable and computationally efficient for $d \gg N$.

---

## 3. t-SNE & The Crowding Problem

Non-linear projection aiming to match neighborhood probability distributions.

### Probability Mappings
*   **High-Dimensional (Gaussian):**
    $$p_{ij} = \frac{p_{j|i} + p_{i|j}}{2N}, \quad p_{j|i} = \frac{\exp(-\|\mathbf{x}_i - \mathbf{x}_j\|^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-\|\mathbf{x}_i - \mathbf{x}_k\|^2 / 2\sigma_i^2)}$$
*   **Low-Dimensional (Student-t / Cauchy):**
    $$q_{ij} = \frac{(1 + \|\mathbf{y}_i - \mathbf{y}_j\|^2)^{-1}}{\sum_{k} \sum_{l \neq k} (1 + \|\mathbf{y}_k - \mathbf{y}_l\|^2)^{-1}}$$
*   **Objective:** Minimize $\text{KL}(P \parallel Q) = \sum_i \sum_j p_{ij} \log \frac{p_{ij}}{q_{ij}}$ via gradient descent.

### The Crowding Problem Resolution
In high dimensions, the volume of a sphere grows exponentially. Mapping points to 2D using a Gaussian distribution forces points to group in a dense mass at the map's center. The heavy-tailed Student-t distribution allows moderate high-dimensional distances to map to larger low-dimensional distances, dispersing the map and resolving crowding.
*   *Note:* t-SNE is non-parametric; it does not support `.transform()` on unseen test samples.
