import numpy as np


def train_perceptron(
    X: np.ndarray, y: np.ndarray, max_updates: int = 1000
) -> tuple[np.ndarray, float, int, bool]:
    """Fits a Rosenblatt Perceptron binary classifier on linearly separable data.

    The updates follow:
        If y_i * (w^T * x_i + b) <= 0:
            w^(t+1) = w^(t) + y_i * x_i
            b^(t+1) = b^(t) + y_i

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        y: Target label array of shape (n_samples,) containing values in {-1,
          1}.
        max_updates: Maximum number of weight updates before stopping (preventing
          infinite loops on non-separable data).

    Returns:
        tuple[np.ndarray, float, int, bool]:
            - w: Final weight vector of shape (n_features,).
            - b: Final scalar bias.
            - update_count: Total number of updates performed.
            - converged: True if all samples are correctly classified, False
              otherwise.
    """
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    update_count = 0
    converged = False

    while update_count < max_updates:
        misclassified_found = False

        for i in range(n_samples):
            x_i = X[i]
            y_i = y[i]

            # Compute prediction score: w^T * x_i + b
            score = np.dot(w, x_i) + b

            # Check if misclassified: y_i * score <= 0
            if y_i * score <= 0.0:
                # Update weights and bias
                w += y_i * x_i
                b += y_i
                update_count += 1
                misclassified_found = True

                # Check if we have hit the maximum updates threshold
                if update_count >= max_updates:
                    break

        # If an entire pass over the dataset completes with no misclassified points, we have converged
        if not misclassified_found:
            converged = True
            break

    return w, b, update_count, converged
