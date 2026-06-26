# Ascendrite Revision Card: RNN Gradients & BPTT

## Backpropagation Through Time (BPTT)

*   **Temporal Unfolding:** The loss $J$ is summed over steps: $J = \sum_{t=1}^T J_t$. Gradients for shared weights are summed temporally:
    $$\frac{\partial J}{\partial \mathbf{W}_{hh}} = \sum_{t=1}^T \frac{\partial J_t}{\partial \mathbf{W}_{hh}}$$
*   **Chain Rule Pathway:** The gradient of step loss $J_t$ with respect to the recurrent weights depends on all previous hidden states:
    $$\frac{\partial J_t}{\partial \mathbf{W}_{hh}} = \sum_{k=1}^t \frac{\partial J_t}{\partial \mathbf{h}_t} \cdot \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} \cdot \frac{\partial \mathbf{h}_k}{\partial \mathbf{W}_{hh}}$$

## Vanishing & Exploding Gradients Proof

*   **Temporal Transition Jacobian:** The gradient flow term is a product of Jacobian matrices:
    $$\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} = \prod_{i=k+1}^t \frac{\partial \mathbf{h}_i}{\partial \mathbf{h}_{i-1}} = \prod_{i=k+1}^t \left( \operatorname{diag}(1 - \tanh^2(\mathbf{z}_i)) \cdot \mathbf{W}_{hh}^\top \right)$$
*   **Numerical Limits:** The norm of the gradient is bounded by:
    $$\left\lVert \frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} \right\rVert \le (\gamma \lVert \mathbf{W}_{hh} \rVert)^{t-k}$$
    Where $\gamma \le 1.0$ is the activation derivative bound.
    *   *Vanishing:* If $\gamma \lVert \mathbf{W}_{hh} \rVert < 1$, gradients decay exponentially to 0 as temporal distance $(t-k)$ increases, losing long-term dependencies.
    *   *Exploding:* If spectral radius of $\mathbf{W}_{hh} > 1$, gradients grow exponentially, causing numerical overflow (NaNs).

## Gradient Norm Clipping

*   **Formulation:** Limits gradient magnitudes while preserving vector direction:
    $$\mathbf{g}_{\text{clip}} = \min\left(1, \frac{\theta}{\lVert \mathbf{g} \rVert_2}\right) \mathbf{g}$$
*   *Note:* Clipping does not solve vanishing gradients; it only prevents gradient explosion. Gated architectures (LSTMs/GRUs) are required to address vanishing gradients.
