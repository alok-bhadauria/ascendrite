import numpy as np


def compute_focal_loss(
    y_true: np.ndarray, y_pred_probs: np.ndarray, gamma: float = 2.0, alpha: float = 0.25
) -> float:
    """Computes the binary Focal Loss between true labels and prediction probabilities.

    Formula:
        FL(p_t) = -alpha_t * (1 - p_t)^gamma * log(p_t)
        where p_t = y_pred_probs if y_true = 1 else (1 - y_pred_probs)

    Args:
        y_true: Binary ground-truth array of shape (n_samples,) with values in {0, 1}.
        y_pred_probs: Model prediction probabilities of shape (n_samples,).
        gamma: The focusing parameter (gamma >= 0) to down-weight easy examples.
        alpha: Class balancing weight for y=1 (1-alpha is used for y=0).

    Returns:
        float: Scalar loss value.
    """
    # Clip predictions to prevent numerical underflow and NaN values from log(0)
    eps = 1e-15
    y_pred_probs = np.clip(y_pred_probs, eps, 1.0 - eps)

    # Compute p_t
    p_t = np.where(y_true == 1, y_pred_probs, 1.0 - y_pred_probs)

    # Compute alpha_t
    alpha_t = np.where(y_true == 1, alpha, 1.0 - alpha)

    # Compute Focal Loss components
    loss_elements = -alpha_t * ((1.0 - p_t) ** gamma) * np.log(p_t)

    return float(np.mean(loss_elements))


def custom_smote(X: np.ndarray, y: np.ndarray, k_neighbors: int = 5, oversampling_ratio: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """Generates synthetic samples for the minority class (assumed to be class 1) using SMOTE.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        y: Binary label vector of shape (n_samples,) where class 1 is the minority class.
        k_neighbors: Number of nearest neighbors to search in minority class.
        oversampling_ratio: The ratio of synthetic samples to generate relative to minority class count.
                            e.g. 1.0 means generate new samples equal to original minority count.

    Returns:
        tuple: (X_resampled, y_resampled) containing original and synthetic observations.
    """
    minority_mask = y == 1
    X_minority = X[minority_mask]
    n_minority, n_features = X_minority.shape

    if n_minority < 2:
        raise ValueError("SMOTE requires at least 2 minority class samples.")

    # Calculate how many synthetic samples to generate
    n_synthetic = int(n_minority * oversampling_ratio)
    synthetic_samples = np.zeros((n_synthetic, n_features))

    # Perform pairwise Euclidean distance computation for minority samples
    # ||a - b||^2 = ||a||^2 + ||b||^2 - 2 * a . b
    sq_norms = np.sum(X_minority ** 2, axis=1, keepdims=True)
    dists = sq_norms + sq_norms.T - 2 * (X_minority @ X_minority.T)
    # Ensure no floating point precision negatives
    dists = np.sqrt(np.maximum(dists, 0.0))

    # For each minority sample, find its k-nearest neighbors in minority class
    # Sort distances and ignore the first index since distance to self is 0
    neighbors_idx = np.argsort(dists, axis=1)[:, 1 : k_neighbors + 1]

    for i in range(n_synthetic):
        # Choose a random index from the original minority samples
        sample_idx = np.random.randint(0, n_minority)
        x_i = X_minority[sample_idx]

        # Select a random neighbor index from the k-nearest neighbors of x_i
        neighbor_pool = neighbors_idx[sample_idx]
        random_neighbor_idx = np.random.choice(neighbor_pool)
        x_nn = X_minority[random_neighbor_idx]

        # Interpolate a synthetic point
        lambda_val = np.random.rand()
        synthetic_samples[i] = x_i + lambda_val * (x_nn - x_i)

    # Stack original and synthetic observations
    X_resampled = np.vstack([X, synthetic_samples])
    y_resampled = np.concatenate([y, np.ones(n_synthetic, dtype=y.dtype)])

    return X_resampled, y_resampled
