import numpy as np


class Var:
    """A variable node in the computational graph, holding data and gradients."""

    def __init__(self, data, requires_grad=False, creator=None):
        self.data = np.asarray(data, dtype=float)
        self.requires_grad = requires_grad
        self.creator = creator
        self.grad = None
        if self.requires_grad:
            self.grad = np.zeros_like(self.data)

    def backward(self, grad=None):
        """Triggers backpropagation."""
        if not self.requires_grad:
            return

        if grad is None:
            if self.data.size == 1:
                grad = np.ones_like(self.data)
            else:
                raise RuntimeError("Grad must be specified for non-scalars")

        if self.grad is None:
            self.grad = grad
        else:
            self.grad += grad

        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                if v.creator is not None:
                    for parent in v.creator.inputs:
                        build_topo(parent)
                    topo.append(v)

        build_topo(self)

        for v in reversed(topo):
            if v.creator is None:
                continue

            inputs_grads = v.creator.backward(v.grad)
            if not isinstance(inputs_grads, tuple):
                inputs_grads = (inputs_grads,)

            for parent, g in zip(v.creator.inputs, inputs_grads):
                if parent.requires_grad and g is not None:
                    if parent.grad is None:
                        parent.grad = np.zeros_like(parent.data)
                    parent.grad += g


class Function:
    """Base class for autograd operations."""

    @classmethod
    def apply(cls, *args):
        inputs = []
        for arg in args:
            if not isinstance(arg, Var):
                inputs.append(Var(arg))
            else:
                inputs.append(arg)

        ctx = cls()
        ctx.inputs = inputs

        raw_inputs = [i.data for i in inputs]
        out_data = ctx.forward(*raw_inputs)

        requires_grad = any(i.requires_grad for i in inputs)
        out = Var(out_data, requires_grad=requires_grad, creator=ctx)
        return out


class CustomSigmoid(Function):
    """Practice task: Implement a numerically stable custom Sigmoid autograd operator.

    Includes clipping inputs to avoid overflow errors.
    """

    def forward(self, x):
        """Computes the forward pass.

        Saves output in context for the backward pass.
        """
        # Save input x to context
        self.x = x

        # Compute sigmoid using numerically stable formula
        # Clip inputs to prevent float overflow under exponentiation
        x_clipped = np.clip(self.x, -500, 500)
        self.out = 1.0 / (1.0 + np.exp(-x_clipped))
        return self.out

    def backward(self, grad_output):
        """Computes the backward pass vector-Jacobian product.

        dJ/dx = grad_output * sigmoid(x) * (1 - sigmoid(x))
        """
        # Return dJ/dx using saved forward output self.out
        dx = grad_output * (self.out * (1.0 - self.out))
        return dx


if __name__ == "__main__":
    print("--- Running Custom Sigmoid Autograd Practice ---")

    # Initialize variable and input array
    x_val = np.array([-1.0, 0.0, 2.0])
    x = Var(x_val, requires_grad=True)

    # Execute custom sigmoid function
    y = CustomSigmoid.apply(x)
    print("Forward output y:", y.data)

    # Expected forward output
    expected_y = 1.0 / (1.0 + np.exp(-x_val))
    assert np.allclose(y.data, expected_y), "Forward pass output mismatch!"

    # Execute backward pass (simulating incoming unit gradients)
    grad_init = np.ones_like(y.data)
    y.backward(grad_init)
    print("Backward input gradient dx:", x.grad)

    # Expected backward gradient: dy/dx = y * (1 - y)
    expected_dx = expected_y * (1.0 - expected_y)
    assert np.allclose(x.grad, expected_dx), "Backward pass gradient mismatch!"

    print("\n  [PASS] Custom Sigmoid Autograd checks passed successfully.")
