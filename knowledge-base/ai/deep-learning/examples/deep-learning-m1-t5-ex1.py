import numpy as np


class Var:
    """A variable representing a node in the computational graph.

    Carries a tensor value, tracks gradients, and maintains a reference to the
    operation creator that produced it.
    """

    def __init__(self, data, requires_grad=False, creator=None):
        self.data = np.asarray(data, dtype=float)
        self.requires_grad = requires_grad
        self.creator = creator
        self.grad = None
        if self.requires_grad:
            self.grad = np.zeros_like(self.data)

    def backward(self, grad=None):
        """Triggers backpropagation starting from this node.

        Performs a topological sort on the computational graph to update
        gradients in reverse execution order.
        """
        if not self.requires_grad:
            return

        # Initialize gradient for scalar loss
        if grad is None:
            if self.data.size == 1:
                grad = np.ones_like(self.data)
            else:
                raise RuntimeError(
                    "Grad must be specified for non-scalar outputs"
                )

        # Accumulate gradient
        if self.grad is None:
            self.grad = grad
        else:
            self.grad += grad

        # 1. Topological Sort of nodes
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

        # 2. Backpropagate in reverse topological order
        for v in reversed(topo):
            if v.creator is None:
                continue

            # Compute gradients of inputs by passing downstream gradient to backward
            inputs_grads = v.creator.backward(v.grad)
            if not isinstance(inputs_grads, tuple):
                inputs_grads = (inputs_grads,)

            # Propagate gradients back to the creator's inputs
            for parent, g in zip(v.creator.inputs, inputs_grads):
                if parent.requires_grad and g is not None:
                    if parent.grad is None:
                        parent.grad = np.zeros_like(parent.data)
                    parent.grad += g

    def __add__(self, other):
        return Add.apply(self, other)

    def __mul__(self, other):
        return Mul.apply(self, other)

    def matmul(self, other):
        return MatMul.apply(self, other)

    def __repr__(self):
        return f"Var({self.data.tolist()}, requires_grad={self.requires_grad})"


class Function:
    """Base class for custom autograd functions.

    Each subclass implements a forward mapping and a backward Vector-Jacobian Product (VJP).
    """

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

        # Extract raw arrays
        raw_inputs = [i.data for i in inputs]
        out_data = ctx.forward(*raw_inputs)

        # Determine gradient tracking requirements
        requires_grad = any(i.requires_grad for i in inputs)

        # Create output node holding pointer to this operation node (creator)
        out = Var(out_data, requires_grad=requires_grad, creator=ctx)
        return out


class Add(Function):
    """Differentiable Addition Operator."""

    def forward(self, x, y):
        return x + y

    def backward(self, grad_output):
        return grad_output, grad_output


class Mul(Function):
    """Differentiable Element-wise Multiplication Operator."""

    def forward(self, x, y):
        self.x = x
        self.y = y
        return x * y

    def backward(self, grad_output):
        # Derivative of xy w.r.t x is y; w.r.t y is x
        return grad_output * self.y, grad_output * self.x


class MatMul(Function):
    """Differentiable Matrix Multiplication Operator."""

    def forward(self, X, W):
        self.X = X
        self.W = W
        return X @ W

    def backward(self, grad_output):
        # y = X @ W
        # dy/dX = grad_output @ W.T
        # dy/dW = X.T @ grad_output
        dX = grad_output @ self.W.T
        dW = self.X.T @ grad_output
        return dX, dW


class CustomReLU(Function):
    """Custom implementation of Rectified Linear Unit (ReLU) with Autograd tracking."""

    def forward(self, x):
        self.x = x
        return np.maximum(0.0, x)

    def backward(self, grad_output):
        # dJ/dx = grad_output * f'(x)
        # f'(x) is 1 for x > 0, 0 otherwise
        dx = grad_output * (self.x > 0).astype(float)
        return dx


if __name__ == "__main__":
    print("--- Autograd Engine Test ---")

    # Define inputs and weights (simulating a single neural network layer)
    # X shape: (1, 3) (batch of 1, 3 features)
    X = Var([[1.0, -2.0, 3.0]], requires_grad=False)
    # W shape: (3, 2) (weights mapping 3 inputs to 2 hidden units)
    W = Var([[0.5, -0.1], [1.2, 0.4], [-0.8, 1.5]], requires_grad=True)
    # b shape: (1, 2)
    b = Var([[0.1, 0.2]], requires_grad=True)

    # 1. Forward Pass: z = X @ W + b
    z = X.matmul(W) + b
    print("Pre-activation z:", z.data)

    # 2. Apply Custom ReLU: a = ReLU(z)
    a = CustomReLU.apply(z)
    print("Post-activation a:", a.data)

    # 3. Compute loss (sum of elements for simplicity)
    loss = Add.apply(a, 0.0)  # Pass through identity for loss tracking
    loss_sum = Var(np.sum(loss.data), requires_grad=True)

    # Run backward pass
    # Since we want to optimize the sum of activations: J = a_1 + a_2
    # The starting gradient vector is ones matching the output shape of 'a'
    grad_init = np.ones_like(a.data)
    a.backward(grad_init)

    print("\nCalculated Gradients:")
    print("  dLoss/dW:\n", W.grad)
    print("  dLoss/db:\n", b.grad)

    # Expected values verification:
    # z = [1.0*0.5 + -2.0*1.2 + 3.0*-0.8 + 0.1, 1.0*-0.1 + -2.0*0.4 + 3.0*1.5 + 0.2]
    # z = [0.5 - 2.4 - 2.4 + 0.1, -0.1 - 0.8 + 4.5 + 0.2]
    # z = [-4.2, 3.8]
    # a = ReLU(z) = [0.0, 3.8]
    # Under backward, local gradient of ReLU is [0.0, 1.0]
    # Input gradient to matrix multiplication is grad_init * local_grad = [1.0, 1.0] * [0.0, 1.0] = [0.0, 1.0]
    # dW = X.T @ [0.0, 1.0] = [[1.0], [-2.0], [3.0]] @ [[0.0, 1.0]] = [[0.0, 1.0], [0.0, -2.0], [0.0, 3.0]]
    # db = [0.0, 1.0]

    expected_dW = np.array([[0.0, 1.0], [0.0, -2.0], [0.0, 3.0]])
    expected_db = np.array([[0.0, 1.0]])

    assert np.allclose(
        W.grad, expected_dW
    ), f"W gradients mismatch! Got: {W.grad}"
    assert np.allclose(
        b.grad, expected_db
    ), f"b gradients mismatch! Got: {b.grad}"
    print("\n  [PASS] Custom Autograd outputs and gradients match analytical proofs.")
