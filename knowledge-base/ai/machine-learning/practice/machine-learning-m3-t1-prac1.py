import numpy as np


def fit_ridge_regression(
    X: np.ndarray, y: np.ndarray, lam: float
) -> np.ndarray:
    """Solves Ridge Regression: (X.T * X + lam * I)^-1 * X.T * y.

    Rules:
    1. Do not penalize the bias parameter (first index of weights).
    2. Add bias column (vector of ones) to X as the first column.
    """
    n_samples, n_features = X.shape
    X_bias = np.hstack([np.ones((n_samples, 1)), X])
    d_dimensions = n_features + 1

    # Penalty matrix (bias is not regularized)
    I_penalty = lam * np.eye(d_dimensions)
    I_penalty[0, 0] = 0.0

    XtX_reg = X_bias.T @ X_bias + I_penalty
    XtY = X_bias.T @ y

    return np.linalg.solve(XtX_reg, XtY)
