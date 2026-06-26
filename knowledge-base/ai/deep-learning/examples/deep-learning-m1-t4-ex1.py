import numpy as np


class SimpleMLP:
    """A 3-layer MLP (Input, Hidden, Output) with ReLU hidden activation and Sigmoid

    output activation, implementing forward and backward passes from scratch.
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        np.random.seed(42)
        # Xavier-style initialization
        self.W1 = (
            np.random.randn(hidden_dim, input_dim) * np.sqrt(2.0 / input_dim)
        )
        self.b1 = np.zeros((hidden_dim, 1))
        self.W2 = (
            np.random.randn(output_dim, hidden_dim) * np.sqrt(2.0 / hidden_dim)
        )
        self.b2 = np.zeros((output_dim, 1))

    def relu(self, z: np.ndarray) -> np.ndarray:
        return np.maximum(0.0, z)

    def relu_deriv(self, z: np.ndarray) -> np.ndarray:
        return (z > 0).astype(float)

    def sigmoid(self, z: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

    def sigmoid_deriv(self, a: np.ndarray) -> np.ndarray:
        return a * (1.0 - a)

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, dict]:
        """Runs the forward pass for a single sample x of shape (input_dim, 1)."""
        z1 = self.W1 @ x + self.b1
        a1 = self.relu(z1)
        z2 = self.W2 @ a1 + self.b2
        a2 = self.sigmoid(z2)

        cache = {"x": x, "z1": z1, "a1": a1, "z2": z2, "a2": a2}
        return a2, cache

    def backward(self, cache: dict, y: np.ndarray) -> dict:
        """Computes gradients using analytical backpropagation equations."""
        x = cache["x"]
        z1 = cache["z1"]
        a1 = cache["a1"]
        a2 = cache["a2"]

        # Mean Squared Error Loss: J = 0.5 * ||a2 - y||^2
        # dJ/da2 = a2 - y
        dJ_da2 = a2 - y

        # Output layer delta: delta2 = dJ/dz2 = dJ/da2 * da2/dz2
        delta2 = dJ_da2 * self.sigmoid_deriv(a2)

        # Gradients for W2 and b2
        dW2 = delta2 @ a1.T
        db2 = delta2

        # Hidden layer delta: delta1 = (W2^T * delta2) * f'(z1)
        delta1 = (self.W2.T @ delta2) * self.relu_deriv(z1)

        # Gradients for W1 and b1
        dW1 = delta1 @ x.T
        db1 = delta1

        return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}

    def compute_loss(self, pred: np.ndarray, y: np.ndarray) -> float:
        return 0.5 * np.sum((pred - y) ** 2)


def check_gradients():
    """Verifies that the analytical gradients derived from backpropagation

    match the numerical gradients computed via finite differences.
    """
    input_dim = 4
    hidden_dim = 5
    output_dim = 2

    mlp = SimpleMLP(input_dim, hidden_dim, output_dim)

    # Single sample
    x = np.random.randn(input_dim, 1)
    y = np.random.rand(output_dim, 1)

    # Analytical Gradients
    pred, cache = mlp.forward(x)
    grads = mlp.backward(cache, y)

    # Numerical Gradients check via finite differences
    epsilon = 1e-6
    parameters = ["W1", "b1", "W2", "b2"]

    print("--- Starting Gradient Checking ---")
    for param_name in parameters:
        param = getattr(mlp, param_name)
        analytical_grad = grads["d" + param_name]
        numerical_grad = np.zeros_like(param)

        # Perturb each element of the parameter matrix
        it = np.nditer(param, flags=["multi_index"], op_flags=["readwrite"])
        while not it.finished:
            idx = it.multi_index
            original_val = param[idx]

            # f(theta + epsilon)
            param[idx] = original_val + epsilon
            pred_plus, _ = mlp.forward(x)
            loss_plus = mlp.compute_loss(pred_plus, y)

            # f(theta - epsilon)
            param[idx] = original_val - epsilon
            pred_minus, _ = mlp.forward(x)
            loss_minus = mlp.compute_loss(pred_minus, y)

            # Reset parameter
            param[idx] = original_val

            # Two-sided numerical gradient formula
            numerical_grad[idx] = (loss_plus - loss_minus) / (2 * epsilon)
            it.iternext()

        # Compute relative difference
        numerator = np.linalg.norm(analytical_grad - numerical_grad)
        denominator = np.linalg.norm(analytical_grad) + np.linalg.norm(
            numerical_grad
        )
        rel_diff = numerator / denominator

        print(f"Parameter: {param_name}")
        print(f"  Analytical Norm: {np.linalg.norm(analytical_grad):.6f}")
        print(f"  Numerical Norm:  {np.linalg.norm(numerical_grad):.6f}")
        print(f"  Relative Diff:   {rel_diff:.4e}")

        # Assert threshold compatibility
        assert (
            rel_diff < 1e-7
        ), f"Gradient check failed for {param_name}! Diff: {rel_diff}"
        print(f"  [PASS] Gradient check successful for {param_name}.\n")

    print("All backpropagation gradients verified successfully!")


if __name__ == "__main__":
    check_gradients()
