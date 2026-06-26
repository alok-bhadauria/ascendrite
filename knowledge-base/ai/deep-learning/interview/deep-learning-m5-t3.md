# Ascendrite Interview Prep: Generative Adversarial Networks (GANs)

## Q1: Derive the optimal discriminator $D^*_G(\mathbf{x})$ in terms of $p_{\text{data}}(\mathbf{x})$ and $p_g(\mathbf{x})$ for a fixed generator $G$.

### Standard Answer
For a fixed generator $G$, the discriminator's objective is to maximize the minimax value function:
$$V(D, G) = \mathbb{E}_{\mathbf{x} \sim p_{\text{data}}} [\log D(\mathbf{x})] + \mathbb{E}_{\mathbf{z} \sim p_{\mathbf{z}}} [\log (1 - D(G(\mathbf{z})))]$$

We can rewrite the expectation over noise $\mathbf{z}$ as an expectation over the generated distribution $p_g(\mathbf{x})$:
$$V(D, G) = \int_{\mathbf{x}} p_{\text{data}}(\mathbf{x}) \log D(\mathbf{x}) d\mathbf{x} + \int_{\mathbf{x}} p_g(\mathbf{x}) \log (1 - D(\mathbf{x})) d\mathbf{x}$$

Combine the integrals:
$$V(D, G) = \int_{\mathbf{x}} \left( p_{\text{data}}(\mathbf{x}) \log D(\mathbf{x}) + p_g(\mathbf{x}) \log (1 - D(\mathbf{x})) \right) d\mathbf{x}$$

To find the optimal discriminator $D^*(\mathbf{x})$ that maximizes this value, we take the partial derivative of the integrand with respect to $D(\mathbf{x})$ for a specific coordinate $\mathbf{x}$, and set it to zero.
Let $y = D(\mathbf{x})$, $a = p_{\text{data}}(\mathbf{x})$, and $b = p_g(\mathbf{x})$. The objective is to maximize:
$$f(y) = a \log y + b \log(1 - y)$$

Take the derivative with respect to $y$:
$$f'(y) = \frac{a}{y} - \frac{b}{1 - y}$$

Set the derivative to 0:
$$\frac{a}{y} = \frac{b}{1 - y} \implies a(1 - y) = by \implies a - ay = by \implies a = (a+b)y$$

Solving for $y$:
$$y = \frac{a}{a+b}$$

Substituting the probability functions back:
$$D^*_G(\mathbf{x}) = \frac{p_{\text{data}}(\mathbf{x})}{p_{\text{data}}(\mathbf{x}) + p_g(\mathbf{x})}$$

This completes the proof of the optimal discriminator.

---

## Q2: Why does the minimax objective $\min_G \max_D V(D, G)$ cause vanishing gradients for the generator early in training? What is the 'non-saturating heuristic' solution?

### Standard Answer
Early in training, the generator $G$ is poorly trained, generating samples that look nothing like the data. The discriminator $D$ easily classifies all generated samples as fake:
$$D(G(\mathbf{z})) \approx 0 \quad \text{for all } \mathbf{z}$$

Under the minimax objective, the generator tries to minimize:
$$\mathcal{L}_G = \log(1 - D(G(\mathbf{z})))$$

Let's look at the gradient of this loss with respect to the discriminator's output $a = D(G(\mathbf{z}))$:
$$\frac{d}{da} \log(1 - a) = -\frac{1}{1 - a}$$

When $a \approx 0$, this derivative is near $-1.0$. However, the gradient passed to the generator's weight updates is scaled by the activation gradients of the discriminator's layers. Because the discriminator is highly confident, its pre-activation values are extremely negative, causing the sigmoid activation to saturate and output virtually zero gradients. The generator receives no learning signals, causing training to stall.

**The Non-Saturating Heuristic:**
Instead of minimizing the probability of being classified as fake ($\log(1 - D(G(\mathbf{z})))$), the generator is trained to **maximize** the probability of being classified as real:
$$\mathcal{L}_G^{\text{heuristic}} = -\log D(G(\mathbf{z}))$$

Let's compute the derivative of this heuristic loss with respect to $a = D(G(\mathbf{z}))$:
$$\frac{d}{da} (-\log a) = -\frac{1}{a}$$

When the generator is poor ($a \approx 0$), the term $-\frac{1}{a}$ approaches $-\infty$. This provides extremely large, strong gradients early in training, accelerating optimization when the generator is poor and resolving the vanishing gradient problem.

---

## Q3: What is Mode Collapse in GANs? Why does it occur, and what techniques mitigate it?

### Standard Answer
**Mode Collapse** is a common failure state in GAN training where the generator learns to produce samples from only a single or a few categories (modes) of the data distribution, completely ignoring the rest of the target diversity. For example, if trained on MNIST (numbers 0 to 9), the generator might collapse to producing only a highly realistic number '7', failing to generate any other digits.

**Why it occurs:**
The standard GAN value function optimizes the coordinate states independently:
$$\min_G \max_D V(D, G)$$
The objective does not contain an explicit diversity or entropy penalty on the generated distribution. If the generator discovers a specific mode that consistently fools the discriminator, the optimal move for $G$ is to map all input noise vectors $\mathbf{z}$ to that single mode. The discriminator will then adapt to classify that mode as fake, causing the generator to jump to another single mode (a phenomenon called "cycling modes" or "cat-and-mouse game"), without ever learning the full distribution.

**Mitigation Techniques:**
1.  **Wasserstein GAN (WGAN-GP):** Replaces the Jensen-Shannon divergence with the Earth Mover's Distance, which provides continuous, smooth gradients everywhere, preventing saturations that lead to mode collapse.
2.  **Unrolled GANs:** Updates the generator based on a preview of the discriminator's future states (unrolling the updates), preventing the generator from exploiting temporary discriminator weaknesses.
3.  **Minibatch Discrimination:** Allows the discriminator to compare samples within a mini-batch to detect lack of diversity, penalizing the generator if generated samples are too similar.
