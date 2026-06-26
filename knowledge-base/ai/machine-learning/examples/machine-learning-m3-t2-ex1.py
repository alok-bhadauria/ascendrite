import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Computes the numerically stable sigmoid activation function."""
    return 1.0 / (1.0 + np.exp(-np.clip(z, -250, 250)))


def fit_logistic_gd(
    X: np.ndarray, y: np.ndarray, lr: float, steps: int
) -> np.ndarray:
    """Fits logistic regression using first-order Gradient Descent."""
    n_samples, n_features = X.shape
    # Add bias dimension
    X_bias = np.hstack([np.ones((n_samples, 1)), X])
    weights = np.zeros(n_features + 1)

    for _ in range(steps):
        # Forward pass
        predictions = sigmoid(X_bias @ weights)

        # Gradient calculation
        gradient = (X_bias.T @ (predictions - y)) / n_samples

        # Parameter update
        weights -= lr * gradient

    return weights


def fit_logistic_irls(
    X: np.ndarray, y: np.ndarray, max_iter: int, tol: float = 1e-6
) -> np.ndarray:
    """Fits logistic regression using second-order IRLS (Newton-Raphson)."""
    n_samples, n_features = X.shape
    X_bias = np.hstack([np.ones((n_samples, 1)), X])
    weights = np.zeros(n_features + 1)

    for _ in range(max_iter):
        predictions = sigmoid(X_bias @ weights)

        # Variance diagonal matrix elements (clipping to prevent singular matrix)
        variances = np.clip(predictions * (1.0 - predictions), 1e-5, 0.25)

        # Hessian matrix calculation: X^T * S * X
        Hessian = (X_bias.T * variances) @ X_bias

        # Gradient vector: X^T * (p - y)
        gradient = X_bias.T @ (predictions - y)

        # Solve for Newton step: H * delta = -gradient
        try:
            delta = np.linalg.solve(Hessian, -gradient)
        except np.linalg.LinAlgError:
            # Fallback to pseudo-inverse if Hessian is ill-conditioned
            delta = np.linalg.pinv(Hessian) @ -gradient

        weights += delta

        # Check convergence
        if np.linalg.norm(delta) < tol:
            break

    return weights
