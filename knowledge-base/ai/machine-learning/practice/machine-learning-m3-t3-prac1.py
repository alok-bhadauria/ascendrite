import numpy as np


def predict_knn_minkowski(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_query: np.ndarray,
    k: int,
    p: float,
) -> np.ndarray:
    """Predicts the class labels for X_query using K-Nearest Neighbors with Minkowski distance.

    Args:
        X_train: Training feature matrix of shape (n_samples, n_features).
        y_train: Training labels of shape (n_samples,).
        X_query: Query feature matrix of shape (n_queries, n_features).
        k: Number of nearest neighbors to consider.
        p: The order of Minkowski distance.

    Returns:
        np.ndarray: Predicted labels of shape (n_queries,).

    Notes:
        - Minkowski distance: D_p(x1, x2) = (sum(|x1 - x2|^p))^(1/p)
        - For tie-breaking in majority voting, select the smallest class label.
    """
    n_queries = X_query.shape[0]
    predictions = np.zeros(n_queries, dtype=y_train.dtype)

    for i in range(n_queries):
        q = X_query[i]
        # Calculate Minkowski distances to all training points
        distances = np.sum(np.abs(X_train - q) ** p, axis=1) ** (1.0 / p)

        # Get indices of the k smallest distances
        k_indices = np.argsort(distances)[:k]

        # Get the labels of the k nearest neighbors
        k_labels = y_train[k_indices]

        # Perform majority voting with tie-breaking
        unique_labels, counts = np.unique(k_labels, return_counts=True)
        max_count = np.max(counts)

        # Find all labels that share the max count
        candidates = unique_labels[counts == max_count]

        # Tie-breaker: select the smallest label value
        predictions[i] = np.min(candidates)

    return predictions
