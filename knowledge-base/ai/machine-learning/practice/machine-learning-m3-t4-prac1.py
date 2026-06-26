import numpy as np


def compute_svm_primal_loss_and_gradient(
    X: np.ndarray, y: np.ndarray, w: np.ndarray, b: float, C: float
) -> tuple[float, np.ndarray, float]:
    """Computes the primal soft-margin SVM objective value (hinge loss + L2 regularization)

    and its subgradients with respect to weights w and bias b.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        y: Labels vector of shape (n_samples,) with values in {-1, 1}.
        w: Weight vector of shape (n_features,).
        b: Bias scalar.
        C: Regularization parameter.

    Returns:
        tuple: (loss_value, grad_w, grad_b)
            - loss_value: float, the computed objective value.
            - grad_w: np.ndarray of shape (n_features,), subgradient with respect to w.
            - grad_b: float, subgradient with respect to b.
    """
    n_samples = X.shape[0]

    # Calculate margins: y_i * (w^T * x_i + b)
    margins = y * (X @ w + b)

    # Compute hinge loss for each sample: max(0, 1 - margin)
    hinge_losses = np.maximum(0.0, 1.0 - margins)

    # Total loss: 0.5 * ||w||_2^2 + C * sum(hinge_loss)
    reg_term = 0.5 * np.dot(w, w)
    total_loss = reg_term + C * np.sum(hinge_losses)

    # Compute subgradients
    # Identify indices where margin violation occurred (1 - y_i*(w^T*x_i + b) > 0)
    violators = hinge_losses > 0.0

    # Subgradient w.r.t w: w - C * sum_{i in V} y_i * x_i
    grad_w = w - C * np.sum(
        (y[violators][:, np.newaxis] * X[violators]), axis=0
    )

    # Subgradient w.r.t b: -C * sum_{i in V} y_i
    grad_b = float(-C * np.sum(y[violators]))

    return total_loss, grad_w, grad_b
