import numpy as np


def compute_log_loss_and_grad(
    X: np.ndarray, y: np.ndarray, w: np.ndarray
) -> tuple[float, np.ndarray]:
    """Computes the binary cross-entropy (Log-Loss) and its gradient

    with respect to weight vector w.

    Ensure:
    1. Numerical stability: clip predictions inside [1e-15, 1 - 1e-15] before
       calculating logarithms to prevent NaN results.
    2. The return is a tuple: (scalar_loss, gradient_vector).
    """
    n_samples = X.shape[0]

    # Calculate probabilities
    z = X @ w
    p = 1.0 / (1.0 + np.exp(-np.clip(z, -250, 250)))

    # Clip probabilities for numerical stability
    p_clipped = np.clip(p, 1e-15, 1 - 1e-15)

    # Compute Log-Loss
    loss = -np.mean(y * np.log(p_clipped) + (1.0 - y) * np.log(1.0 - p_clipped))

    # Compute Gradient vector
    grad = (X.T @ (p - y)) / n_samples

    return loss, grad
