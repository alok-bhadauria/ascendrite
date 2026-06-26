# Ascendrite Revision Card: Autoencoders (AE)

## Architecture Layout

*   **Encoder ($f_{\theta}$):** Maps input space $\mathbf{x} \in \mathbb{R}^D$ to bottleneck latent space $\mathbf{z} \in \mathbb{R}^d$:
    $$\mathbf{z} = \sigma(\mathbf{W}_e \mathbf{x} + \mathbf{b}_e)$$
*   **Decoder ($g_{\phi}$):** Reconstructs original input representation $\hat{\mathbf{x}}$ from latent code $\mathbf{z}$:
    $$\hat{\mathbf{x}} = \sigma(\mathbf{W}_d \mathbf{z} + \mathbf{b}_d)$$
*   **Bottleneck constraint:** Restricting latent dimension $d < D$ forces the network to drop noise and learn salient features.

## Undercomplete vs. Overcomplete

*   **Undercomplete ($d < D$):** Forced compression. If activation functions are linear, the network maps zero-mean inputs to the same subspace as Principal Component Analysis (PCA). Non-linear activations learn non-linear manifolds.
*   **Overcomplete ($d > D$):** Latent dimensions are larger than input. Unregularized, it learns a useless copy identity function. If regularized (e.g. Denoising or Sparsity constraints), it extracts robust features.
*   **Denoising AE (DAE):** Trained to reconstruct clean inputs from corrupted noisy inputs, mapping coordinates back to the stable data manifold.

## Optimization Losses

*   **Mean Squared Error (MSE):** For continuous variables:
    $$J_{\text{MSE}} = \frac{1}{2} \lVert \mathbf{x} - \hat{\mathbf{x}} \rVert_2^2$$
*   **Binary Cross-Entropy (BCE):** For normalized pixel inputs in $[0, 1]$:
    $$J_{\text{BCE}} = -\sum_j \left( x_j \log \hat{x}_j + (1 - x_j) \log (1 - \hat{x}_j) \right)$$
