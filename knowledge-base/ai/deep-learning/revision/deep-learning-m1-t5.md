# Ascendrite Revision Layer: Deep Learning Frameworks (Custom Autograd)

## 1. Graph Execution Paradigms

Deep learning frameworks orchestrate operations using computational graphs:
*   **Static Graph (Define-and-Run):** Enforces a strict separation between graph construction and graph execution. Allows global optimizations like operator fusion and memory allocation planning before execution.
*   **Dynamic Graph (Define-by-Run):** Builds the computational graph on-the-fly during execution (eager execution). Evaluates operations dynamically, supporting native Python control flows (loops, conditionals) and native debugging.

---

## 2. Reverse-Mode Autograd Mathematics

Autograd uses reverse-mode automatic differentiation to compute gradients. We define the adjoint of a variable $x$ as:
$$\bar{x} = \frac{\partial J}{\partial x}$$

For a node implementing $y = g(x)$, given the incoming output gradient $\bar{y}$, the input gradient is the Vector-Jacobian Product (VJP):
$$\bar{x} = \bar{y} \cdot \frac{\partial y}{\partial x} = \bar{y} \cdot g'(x)$$

### Gradient Accumulation Rule
When a tensor splits into multiple operational branches, the gradients of the branch outputs are summed to compute the parent tensor's total gradient:
$$\bar{x} = \sum_{k} \bar{y}_k \frac{\partial y_k}{\partial x}$$

---

## 3. Custom Autograd Operator Design

To implement a custom differentiable operator, subclass the autograd system and define two methods:
1.  **`forward(ctx, inputs)`**:
    *   Computes the forward pass operations.
    *   Saves necessary tensors for the backward pass using `ctx.save_for_backward()`.
2.  **`backward(ctx, grad_output)`**:
    *   Receives the incoming gradient $\mathbf{v} = \frac{\partial J}{\partial \mathbf{y}}$ (of shape $1 \times m$).
    *   Computes the vector-Jacobian product (VJP) to obtain the gradient with respect to inputs: $\frac{\partial J}{\partial \mathbf{x}} = \mathbf{v} \mathbf{J}$ (of shape $1 \times n$).
    *   Returns one gradient per forward input (returns `None` for non-tensor inputs or parameters not requiring gradients).
