# Ascendrite Revision Card: Variational Autoencoders (VAE)

## Probabilistic Latent Spaces

*   **Deterministic vs. Probabilistic:** Deterministic autoencoders map inputs to a single coordinate, leaving unconstrained 'dead zones' in latent space. VAEs map inputs to a Gaussian distribution, making the space continuous and suitable for sampling.
*   **Parameters:** The encoder outputs a mean vector $\boldsymbol{\mu}(\mathbf{x})$ and a log-variance vector $\log(\boldsymbol{\sigma}^2(\mathbf{x}))$.
*   **Log-Variance Rule:** Encoders predict $\log(\boldsymbol{\sigma}^2)$ instead of standard deviation $\boldsymbol{\sigma}$ to allow output range $(-\infty, \infty)$ while ensuring $\boldsymbol{\sigma} = e^{0.5 \log(\boldsymbol{\sigma}^2)}$ remains strictly positive.

## The Reparameterization Trick

*   **The Problem:** Direct sampling $\mathbf{z} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\sigma}^2\mathbf{I})$ is stochastic and has no defined derivative, blocking backpropagation.
*   **The Solution:** Isolate the stochastic element by sampling noise $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ and computing the latent code deterministically:
    $$\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon}$$
*   **Gradient Path:** Because $\boldsymbol{\epsilon}$ is a constant input, the path from $\mathbf{z}$ back to encoder outputs is differentiable:
    $$\frac{\partial \mathbf{z}}{\partial \boldsymbol{\mu}} = I \quad \text{and} \quad \frac{\partial \mathbf{z}}{\partial \boldsymbol{\sigma}} = \operatorname{diag}(\boldsymbol{\epsilon})$$

## Evidence Lower Bound (ELBO) Loss

$$\mathcal{L}_{\text{VAE}} = \mathcal{L}_{\text{reconstruction}} + D_{\text{KL}}(q_{\phi}(\mathbf{z}|\mathbf{x}) \parallel p(\mathbf{z}))$$

1.  **Reconstruction Loss:** Measures reconstruction accuracy (e.g. MSE or BCE).
2.  **KL Divergence:** Regularizes the predicted distribution to match a standard normal prior $\mathcal{N}(\mathbf{0}, \mathbf{I})$.
    *   *Closed-form Gaussian equation:*
        $$D_{\text{KL}} = -\frac{1}{2} \sum_{j=1}^d \left( 1 + \log(\sigma_j^2) - \mu_j^2 - \sigma_j^2 \right)$$
3.  **Balance:** Reconstruction preserves details; KL divergence clusters representations together around the origin to ensure a continuous space.
