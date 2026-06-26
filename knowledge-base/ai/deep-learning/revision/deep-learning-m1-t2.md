# Ascendrite Revision Layer: Activation Functions

## 1. Classical Sigmoidal Functions

### Sigmoid Activation
Maps inputs to $(0, 1)$:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$
$$\sigma'(z) = \sigma(z)(1 - \sigma(z))$$

*   *Vanishing Gradient:* Max gradient is $0.25$ (at $z=0$). In deep networks, gradients shrink rapidly as they propagate backward.
*   *Non-Zero-Centered:* Outputs are strictly positive, forcing zig-zagging parameter updates.

### Hyperbolic Tangent (Tanh)
Maps inputs to $(-1, 1)$:

$$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}} = 2\sigma(2z) - 1$$
$$\tanh'(z) = 1 - \tanh^2(z)$$

*   *Zero-Centered:* Outputs have a mean near $0$, facilitating faster optimization convergence than Sigmoid.
*   *Saturation:* Still suffers from vanishing gradients as $|z| \to \infty$.

---

## 2. Rectified Activations

### Rectified Linear Unit (ReLU)
$$f(z) = \max(0, z)$$
$$f'(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z < 0 \end{cases}$$

*   *Dying ReLU:* If a neuron's activation is negative for all inputs, its gradient is permanently $0.0$, disabling weight updates.
*   *Mitigation:* Leaky ReLU or PReLU.

### Leaky ReLU
Introduces a small negative slope $\alpha \approx 0.01$:

$$f(z) = \max(\alpha z, z)$$
$$f'(z) = \begin{cases} 1 & \text{if } z > 0 \\ \alpha & \text{if } z < 0 \end{cases}$$

---

## 3. Softmax Function

Maps a logit vector $\mathbf{z} \in \mathbb{R}^K$ to a probability distribution $\mathbf{a} \in \mathbb{R}^K$:

$$a_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

### Translation Invariance Property
For any constant $c \in \mathbb{R}$:
$$\operatorname{softmax}(\mathbf{z} + c\mathbf{1}) = \operatorname{softmax}(\mathbf{z})$$

*   *Numerical Stability Implementation:* Subtract the maximum logit ($c = -\max_j z_j$) to ensure all exponentiations are of non-positive numbers (max is $e^0 = 1.0$), preventing floating-point overflow.
