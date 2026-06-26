# Ascendrite Interview Prep: Deep Learning Frameworks

## Q1: Why do modern deep learning frameworks implement reverse-mode automatic differentiation using Vector-Jacobian Products (VJPs) rather than computing the full Jacobian matrix?

### Standard Answer
In typical deep learning systems, we optimize a scalar objective function (the loss, $J \in \mathbb{R}$) with respect to a large number of parameters ($\mathbf{\theta} \in \mathbb{R}^n$). 

If we used forward-mode automatic differentiation, we would track the derivative of all intermediate nodes with respect to each input parameter. This requires $n$ forward evaluations (one for each parameter dimension), which is computationally intractable when $n$ is in the millions or billions.

Using reverse-mode automatic differentiation, we work backward from the scalar loss. For an operation $\mathbf{y} = \mathbf{f}(\mathbf{x})$ where $\mathbf{x} \in \mathbb{R}^n$ and $\mathbf{y} \in \mathbb{R}^m$, the backward pass receives the incoming gradient of the scalar loss with respect to the output, $\mathbf{v} = \frac{\partial J}{\partial \mathbf{y}} \in \mathbb{R}^{1 \times m}$. The backward pass computes:
$$\frac{\partial J}{\partial \mathbf{x}} = \mathbf{v} \mathbf{J} \in \mathbb{R}^{1 \times n}$$
where $\mathbf{J} = \frac{\partial \mathbf{y}}{\partial \mathbf{x}} \in \mathbb{R}^{m \times n}$ is the Jacobian matrix. 

By computing the Vector-Jacobian Product (VJP) directly, the framework maps the output gradient (a vector of size $m$) back to the input gradient (a vector of size $n$) without ever explicitly building or storing the full $m \times n$ Jacobian matrix in memory. This reduces the time complexity of computing the gradients of a scalar loss with respect to all parameters to approximately the same scale as a single forward pass.

---

## Q2: Why does calling `.backward()` on a non-scalar tensor in PyTorch throw a runtime error, and how is it resolved?

### Standard Answer
By design, the mathematical goal of backpropagation in PyTorch is to compute the gradient of a *scalar* loss function $J$ with respect to the model parameters. 

When you call `y.backward()` on a tensor $\mathbf{y}$ that is not a scalar (e.g., shape is $(d_1, d_2)$ instead of containing a single value), the autograd engine does not know what scalar objective it is optimizing. It lacks the starting adjoint $\mathbf{v} = \frac{\partial J}{\partial \mathbf{y}}$ (which would be $1$ if $\mathbf{y}$ was the loss itself) to initialize the reverse-mode traversal.

To resolve this, you must either:
1.  **Reduce the tensor to a scalar** before calling backward by using a reduction operator (e.g., `y.sum().backward()` or `y.mean().backward()`). This implicitly sets the starting gradient to a tensor of ones or scaling factors.
2.  **Provide an explicit gradient argument** to the backward call: `y.backward(gradient=v)`, where `v` is a tensor of the same shape as `y` representing the pre-computed external gradients $\frac{\partial J}{\partial \mathbf{y}}$.

---

## Q3: What is the cause and resolution of memory leaks associated with storing loss values in lists during a training loop?

### Standard Answer
In PyTorch, any tensor resulting from operations on parameters that require gradients carries a reference to the computational graph through its `.grad_fn` attribute. 

If you log the loss value by appending the raw loss tensor directly to a list, like so:
```python
loss_history.append(loss) # Memory leak!
```
you keep a reference to the entire computational graph of that iteration alive in memory. The Python garbage collector cannot reclaim the memory occupied by the cached activations and graph nodes of the forward pass because the list holds a live reference to the terminal node of the graph.

To prevent this memory leak, you must detach the value from the computational graph, or retrieve its python scalar value using `.item()` or `.detach().cpu().numpy()`:
```python
loss_history.append(loss.item()) # Safe: extracts raw python float
```
This breaks the reference to the computational graph, allowing the autograd engine to free the intermediate activations.
