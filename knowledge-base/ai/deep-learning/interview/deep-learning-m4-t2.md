# Ascendrite Interview Prep: RNN Gradients & BPTT

## Q1: Why do Recurrent Neural Networks suffer from vanishing and exploding gradients? Provide a mathematical proof.

### Standard Answer
The hidden state update in an Elman RNN is:
$$\mathbf{h}_i = \tanh(\mathbf{W}_{hh} \mathbf{h}_{i-1} + \mathbf{W}_{xh} \mathbf{x}_i + \mathbf{b}_h)$$

When applying Backpropagation Through Time (BPTT), the gradient of the loss at step $t$ with respect to the state at an earlier step $k$ ($k < t$) is:
$$\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} = \prod_{i=k+1}^t \frac{\partial \mathbf{h}_i}{\partial \mathbf{h}_{i-1}}$$

Let's compute the Jacobian matrix for a single step:
$$\frac{\partial \mathbf{h}_i}{\partial \mathbf{h}_{i-1}} = \operatorname{diag}(1 - \tanh^2(\mathbf{z}_i)) \cdot \mathbf{W}_{hh}^{\top}$$
Where $\mathbf{z}_i$ is the pre-activation input vector.

Substituting this back into the product:
$$\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} = \prod_{i=k+1}^t \left( \operatorname{diag}(1 - \tanh^2(\mathbf{z}_i)) \cdot \mathbf{W}_{hh}^{\top} \right)$$

Let $\gamma$ be the maximum value of the derivative of the activation function (for tanh, $\gamma \le 1.0$). Taking the L2 norm of the gradient matrix product:
$$\left\lVert \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} \right\rVert \le \prod_{i=k+1}^t \gamma \lVert \mathbf{W}_{hh} \rVert_2 = (\gamma \lVert \mathbf{W}_{hh} \rVert_2)^{t-k}$$

**1. Vanishing Gradients:**
If the spectral radius (or maximum eigenvalue) of the recurrent weight matrix $\mathbf{W}_{hh}$ is less than 1 (specifically, if $\gamma \lVert \mathbf{W}_{hh} \rVert_2 < 1$), the term $(\gamma \lVert \mathbf{W}_{hh} \rVert_2)^{t-k}$ decays exponentially to 0 as the distance $(t-k)$ increases. The network cannot propagate error signals back to early steps, losing long-term dependencies.

**2. Exploding Gradients:**
If the spectral radius of $\mathbf{W}_{hh}$ is greater than 1, and the activations do not saturate, the term $(\gamma \lVert \mathbf{W}_{hh} \rVert_2)^{t-k}$ grows exponentially as $(t-k)$ increases. This causes numerical overflow (NaNs) or large weight updates that destabilize training.

---

## Q2: How does Gradient Norm Clipping work? Explain why we clip the norm of the total gradient vector instead of clamping individual gradient elements.

### Standard Answer
**Gradient Norm Clipping** limits the magnitude of the gradient vector if its L2 norm exceeds a specified threshold $\theta$:
$$\mathbf{g}_{\text{clip}} = \min\left(1, \frac{\theta}{\lVert \mathbf{g} \rVert_2}\right) \mathbf{g}$$
Where $\mathbf{g}$ is the concatenated vector of all parameter gradients in the network.

**Why clip by norm instead of clamping element-wise?**
*   **Element-wise clamping** (or value clipping) clamps each element of the gradient independently to a range $[-c, c]$. This changes the **direction** of the gradient vector in parameter space. By altering the vector's angle, optimization steps can drift, slowing convergence.
*   **Norm clipping** scales the entire gradient vector by a constant factor if its norm exceeds $\theta$. This preserves the **direction** of the gradient vector while bounding its step size, ensuring stable optimization.

---

## Q3: Does gradient clipping solve the vanishing gradient problem? If not, what does?

### Standard Answer
No, gradient clipping **does not** solve the vanishing gradient problem. It only prevents gradients from growing too large (exploding).

To resolve the vanishing gradient problem, we use structural changes:
1.  **Gated Architectures (LSTMs and GRUs):** These networks introduce additive cell state update paths controlled by gating channels. Additive paths allow gradients to flow back over long sequences without exponential decay.
2.  **Orthogonal/Identity Initializations:** Initializing the recurrent weight matrix $\mathbf{W}_{hh}$ as an orthogonal matrix ensures its eigenvalues are exactly 1.0, preserving gradient norm scales during backpropagation.
3.  **Alternative Activations:** Using activations like ReLU (which has a derivative of exactly 1.0 for positive inputs) instead of saturating activations like tanh.
