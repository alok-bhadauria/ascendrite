import numpy as np


def solve_ols_scratch(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Computes the closed-form Ordinary Least Squares solution:

    w = (X^T * X)^-1 * X^T * y
    """
    # Add bias dimension
    n_samples = X.shape[0]
    X_bias = np.hstack([np.ones((n_samples, 1)), X])

    # Normal equations
    XtX = X_bias.T @ X_bias
    XtY = X_bias.T @ y

    # Solve linear system
    return np.linalg.solve(XtX, XtY)


def solve_ridge_scratch(
    X: np.ndarray, y: np.ndarray, alpha: float
) -> np.ndarray:
    """Computes the closed-form Ridge Regression solution:

    w = (X^T * X + alpha * I)^-1 * X^T * y
    """
    n_samples, n_features = X.shape
    # Add bias dimension
    X_bias = np.hstack([np.ones((n_samples, 1)), X])
    d_dimensions = n_features + 1

    # Normal equations with L2 penalty matrix (bias is not regularized)
    penalty_matrix = alpha * np.eye(d_dimensions)
    penalty_matrix[0, 0] = 0.0

    XtX = X_bias.T @ X_bias + penalty_matrix
    XtY = X_bias.T @ y

    return np.linalg.solve(XtX, XtY)
