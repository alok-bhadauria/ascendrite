# Ascendrite Revision Layer: Neural Foundations

## 1. Single Neuron Model

An artificial neuron models a biological cell body by performing a weighted linear combination of inputs followed by a non-linear activation mapping:

$$z = \mathbf{w}^{\top}\mathbf{x} + b = \sum_{i=1}^d w_i x_i + b$$
$$y = f(z) = f(\mathbf{w}^{\top}\mathbf{x} + b)$$

*   **Inputs ($\mathbf{x}$):** Dendrites feature vector.
*   **Weights ($\mathbf{w}$):** Synaptic connection strength scaling factors.
*   **Bias ($b$):** Activations threshold shift parameter.
*   **Activation ($f$):** Non-linear mapping function.

---

## 2. Perceptron Convergence Theorem

For a binary classifier $y = \operatorname{sgn}(\mathbf{w}^{\top}\mathbf{x})$ updated on misclassifications via $\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} + y_i \mathbf{x}_i$ where $\mathbf{w}^{(0)} = \mathbf{0}$:

### The Margin Assumption
If data is linearly separable, there exists a unit vector $\mathbf{w}^*$ ($\|\mathbf{w}^*\|_2 = 1$) such that:
$$y_i(\mathbf{w}^{*\top}\mathbf{x}_i) \ge \gamma > 0 \quad \forall i$$

Let $R = \max_i \|\mathbf{x}_i\|_2$ be the maximum boundary of the input space.

### The Bounds of the Convergence Proof
1.  **Lower Bound:** After $k$ updates, Cauchy-Schwarz shows the weight norm grows linearly with updates:
    $$\|\mathbf{w}^{(k)}\|_2 \ge k\gamma$$
2.  **Upper Bound:** Misclassification properties show the weight norm is bounded by the input step sizes:
    $$\|\mathbf{w}^{(k)}\|_2^2 \le k R^2$$
3.  **Maximum Number of Updates:**
    $$k \le \frac{R^2}{\gamma^2}$$
    Since $k$ is bounded, convergence is guaranteed in finite steps.

---

## 3. Multi-Layer Perceptron (MLP)

MLPs stack multiple layers of neurons to represent non-linear decision boundaries.

### Matrix Forward Propagation
For each layer $l \in \{1, \dots, L\}$ with activation function $f^{(l)}$:

$$\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}$$
$$\mathbf{a}^{(l)} = f^{(l)}(\mathbf{z}^{(l)})$$

*   $\mathbf{a}^{(l-1)} \in \mathbb{R}^{d_{l-1}}$: Output of previous layer (where $\mathbf{a}^{(0)} = \mathbf{x}$).
*   $\mathbf{W}^{(l)} \in \mathbb{R}^{d_l \times d_{l-1}}$: Weight matrix mapping dimensions $d_{l-1} \to d_l$.
*   $\mathbf{b}^{(l)} \in \mathbb{R}^{d_l}$: Bias vector.
*   $\mathbf{a}^{(l)} \in \mathbb{R}^{d_l}$: Post-activation output of layer $l$.
