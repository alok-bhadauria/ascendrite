# Ascendrite Interview Prep: Autoencoders (AE)

## Q1: Prove that an undercomplete autoencoder with strictly linear activation functions is equivalent to Principal Component Analysis (PCA).

### Standard Answer
Let $\mathbf{x} \in \mathbb{R}^D$ be a zero-mean input vector. A linear autoencoder projects $\mathbf{x}$ to a lower-dimensional latent space $\mathbf{z} \in \mathbb{R}^d$ ($d < D$), and then reconstructs it as $\hat{\mathbf{x}}$:
$$\mathbf{z} = \mathbf{W}_e \mathbf{x} \quad \text{and} \quad \hat{\mathbf{x}} = \mathbf{W}_d \mathbf{z} = \mathbf{W}_d \mathbf{W}_e \mathbf{x}$$
Where $\mathbf{W}_e \in \mathbb{R}^{d \times D}$ and $\mathbf{W}_d \in \mathbb{R}^{D \times d}$ are the encoder and decoder weight matrices.

The objective is to minimize the Mean Squared Error (MSE) reconstruction loss over a dataset of $N$ samples:
$$\min_{\mathbf{W}_e, \mathbf{W}_d} \frac{1}{N} \sum_{i=1}^N \lVert \mathbf{x}^{(i)} - \mathbf{W}_d \mathbf{W}_e \mathbf{x}^{(i)} \rVert_2^2$$

This is identical to the formulation of low-rank matrix approximation. By the Eckart-Young-Mirsky theorem, the optimal rank-$d$ approximation of the data matrix $\mathbf{X}$ is obtained via the Singular Value Decomposition (SVD).

Let the SVD of the data covariance matrix $\boldsymbol{\Sigma} = \frac{1}{N} \mathbf{X}^{\top}\mathbf{X}$ be $\mathbf{U} \boldsymbol{\Lambda} \mathbf{U}^{\top}$. The projection matrix that minimizes the reconstruction error is:
$$\mathbf{P} = \mathbf{U}_d \mathbf{U}_d^{\top}$$
Where $\mathbf{U}_d \in \mathbb{R}^{D \times d}$ contains the first $d$ principal eigenvectors of $\boldsymbol{\Sigma}$ (the principal components).

In the linear autoencoder, the product matrix $\mathbf{W}_d \mathbf{W}_e$ acts as the projection operator $\mathbf{P}$. At convergence:
$$\mathbf{W}_d \mathbf{W}_e = \mathbf{U}_d \mathbf{U}_d^{\top}$$

This proves that the linear autoencoder projects the data onto the same subspace as PCA.
*Note:* Although the subspace is identical, the individual weights $\mathbf{W}_e$ and $\mathbf{W}_d$ do not necessarily align with the orthogonal principal component vectors unless explicit orthogonality constraints are added to the weights, because any invertible matrix multiplication $\mathbf{W}_e \mathbf{A}$ and $\mathbf{A}^{-1} \mathbf{W}_d$ yields the same reconstruction.

---

## Q2: What is the difference between an Undercomplete and an Overcomplete Autoencoder? How do we prevent an Overcomplete Autoencoder from learning a simple copy function?

### Standard Answer
*   **Undercomplete Autoencoder:** The latent dimension is smaller than the input dimension ($d < D$). The dimension bottleneck forces the network to compress the data, learning the most salient factors of the data manifold.
*   **Overcomplete Autoencoder:** The latent dimension is larger than the input dimension ($d > D$). Since the latent space has more capacity than the input space, the network can easily learn a trivial copy function (identity mapping) without learning any useful feature representations.

**Preventing Trivial Mappings in Overcomplete Autoencoders:**
To force an overcomplete network to learn meaningful representations, we must limit its capacity or regularize its activations:
1.  **Sparsity Constraint (Sparse Autoencoders):** We add a penalty to the loss function that penalizes active latent units (e.g. L1 regularization on activations or KL-divergence relative to a low target sparsity parameter $\rho$):
    $$J_{\text{sparse}} = J_{\text{recon}} + \beta \sum_{j} \text{KL}(\rho \lVert \hat{\rho}_j)$$
    This forces the network to represent each sample using only a small, active subset of hidden units.
2.  **Denoising (Denoising Autoencoders):** We corrupt the input with noise (e.g. masking noise or Gaussian noise) before feeding it to the encoder, but compute the reconstruction loss relative to the clean original input. The network cannot copy inputs because it must learn to project noisy coordinates back onto the clean data manifold.

---

## Q3: When should you use Mean Squared Error (MSE) versus Binary Cross-Entropy (BCE) as the reconstruction loss for an autoencoder?

### Standard Answer
*   **Mean Squared Error (MSE):**
    *   **Applicability:** Continuous, real-valued variables (e.g., audio wave amplitudes, physical sensors, or raw coordinates).
    *   **Assumption:** The reconstruction error is assumed to follow a Gaussian distribution with constant variance.
*   **Binary Cross-Entropy (BCE):**
    *   **Applicability:** Input features are normalized pixel values bounded in the range $[0, 1]$ (e.g., MNIST digit images).
    *   **Assumption:** The input features are treated as independent Bernoulli probabilities. The decoder output layer uses a sigmoid activation to output values in $[0, 1]$, and BCE optimizes the probability likelihood of the pixel state. It converges faster and generates sharper borders for binary/pixel tasks compared to MSE, which tends to produce blurry reconstructions.
