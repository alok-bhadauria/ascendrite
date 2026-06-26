# Ascendrite Revision Card: Generative Adversarial Networks (GANs)

## Adversarial Framework

*   **Generator ($G$):** Projects random noise $\mathbf{z} \sim p_{\mathbf{z}}$ to produce generated samples $G(\mathbf{z})$ to fool the discriminator.
*   **Discriminator ($D$):** A binary classifier mapping inputs to probability $D(\mathbf{x}) \in [0, 1]$ (real vs. fake).
*   **Nash Equilibrium:** At convergence, $p_g = p_{\text{data}}$ and the optimal discriminator outputs exactly $D^*_G(\mathbf{x}) = 0.5$ everywhere.

## Minimax Game Objective

$$\min_G \max_D V(D, G) = \mathbb{E}_{\mathbf{x} \sim p_{\text{data}}} [\log D(\mathbf{x})] + \mathbb{E}_{\mathbf{z} \sim p_{\mathbf{z}}} [\log (1 - D(G(\mathbf{z})))]$$

*   **Optimal Discriminator Proof:** For a fixed generator $G$, the optimal discriminator is:
    $$D^*_G(\mathbf{x}) = \frac{p_{\text{data}}(\mathbf{x})}{p_{\text{data}}(\mathbf{x}) + p_g(\mathbf{x})}$$

## Training Challenges

*   **Vanishing Gradients:** Early in training, $D(G(\mathbf{z})) \approx 0$. The derivative of $\log(1 - D(G(\mathbf{z})))$ vanishes, stalling updates.
    *   *Solution (Non-Saturating Heuristic):* Maximize $\log D(G(\mathbf{z}))$ instead of minimizing $\log(1 - D(G(\mathbf{z})))$, providing large gradients early in training.
*   **Mode Collapse:** A failure mode where the generator outputs samples from only one or few modes of the dataset (e.g. producing only one specific digit), ignoring the rest of the distribution.
*   **Wasserstein GAN (WGAN):** Uses Earth Mover's Distance to resolve training instability by removing the discriminator's output sigmoid and enforcing Lipshitz continuity constraints.
