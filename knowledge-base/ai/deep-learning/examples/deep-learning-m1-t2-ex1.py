import numpy as np


def standard_softmax(z: np.ndarray) -> np.ndarray:
    """Computes standard Softmax (prone to floating-point overflow)."""
    exps = np.exp(z)
    return exps / np.sum(exps)


def stable_softmax(z: np.ndarray) -> np.ndarray:
    """Computes numerically stable Softmax by subtracting the maximum value."""
    # z - max(z) translation invariance
    shifted_z = z - np.max(z)
    exps = np.exp(shifted_z)
    return exps / np.sum(exps)


def relu(z: np.ndarray) -> np.ndarray:
    """Standard ReLU function."""
    return np.maximum(0.0, z)


def relu_derivative(z: np.ndarray) -> np.ndarray:
    """Derivative of standard ReLU."""
    return np.where(z > 0.0, 1.0, 0.0)


def leaky_relu(z: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    """Leaky ReLU function."""
    return np.maximum(alpha * z, z)


def leaky_relu_derivative(z: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    """Derivative of Leaky ReLU."""
    return np.where(z > 0.0, 1.0, alpha)


if __name__ == "__main__":
    # --- 1. Softmax Numerical Stability Test ---
    print("--- 1. Softmax Numerical Stability Test ---")
    large_logits = np.array([1000.0, 1001.0, 1002.0])
    print(f"Large Logits: {large_logits}")

    # Standard Softmax fails
    try:
        std_out = standard_softmax(large_logits)
        print(f"Standard Softmax Output: {std_out}")
    except Exception as e:
        print(f"Standard Softmax failed: {e}")

    # Stable Softmax succeeds
    stable_out = stable_softmax(large_logits)
    print(f"Numerically Stable Softmax Output: {stable_out}")

    # --- 2. Dying ReLU Simulation ---
    print("\n--- 2. Dying ReLU Simulation ---")
    # Suppose a neuron has weights w and bias b
    w = np.array([0.5, -0.5])
    # The bias has been shifted to a large negative value due to a large update
    b_dead = -5.0
    b_leaky = -5.0

    # Incoming batch of samples
    X = np.array([[1.0, 2.0], [2.0, 1.0], [0.5, 0.5]])

    print("Inputs X:\n", X)
    # Compute pre-activations: z = X * w + b
    # All values will be negative
    z_dead = X @ w + b_dead
    print(f"Pre-activations (z): {z_dead}")

    # Forward activations
    a_relu = relu(z_dead)
    a_leaky = leaky_relu(z_dead, alpha=0.01)

    print("\nStandard ReLU activations (Forward):")
    print(a_relu, " (All dead/zero)")

    print("Leaky ReLU activations (Forward):")
    print(a_leaky, " (Active non-zero)")

    # Backward pass gradients
    # Suppose the downstream gradient dL/da is [1.0, 1.0, 1.0]
    dL_da = np.ones(3)

    grad_w_relu = (dL_da * relu_derivative(z_dead)) @ X
    grad_b_relu = np.sum(dL_da * relu_derivative(z_dead))

    grad_w_leaky = (dL_da * leaky_relu_derivative(z_dead)) @ X
    grad_b_leaky = np.sum(dL_da * leaky_relu_derivative(z_dead))

    print("\nStandard ReLU Weight Gradient (dL/dw):", grad_w_relu)
    print("Standard ReLU Bias Gradient (dL/db):  ", grad_b_relu)
    print("  -> Parameters will NEVER update again.")

    print("\nLeaky ReLU Weight Gradient (dL/dw):   ", grad_w_leaky)
    print("Leaky ReLU Bias Gradient (dL/db):     ", grad_b_leaky)
    print("  -> Non-zero gradients allow weights to recover.")
