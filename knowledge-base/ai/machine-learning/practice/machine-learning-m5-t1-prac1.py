import numpy as np


def compute_point_silhouette(
    X: np.ndarray, labels: np.ndarray, sample_idx: int
) -> float:
    """Computes the Silhouette Coefficient for a single observation in the dataset.

    Formula:
        s(x) = (b(x) - a(x)) / max(a(x), b(x))
        where:
            - a(x) is the mean intra-cluster distance between x and all other points in the same cluster.
            - b(x) is the mean distance from x to the points of the nearest neighboring cluster.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        labels: Cluster assignment labels of shape (n_samples,).
        sample_idx: Index of the query sample.

    Returns:
        float: Silhouette coefficient in range [-1, 1]. Returns 0.0 if the sample's
               assigned cluster contains only a single point.
    """
    n_samples = X.shape[0]
    query_point = X[sample_idx]
    query_label = labels[sample_idx]

    # 1. Identify query's cluster points
    intra_mask = (labels == query_label)
    # Exclude the query point itself from intra-cluster distance calculations
    intra_mask[sample_idx] = False

    n_intra = np.sum(intra_mask)
    if n_intra == 0:
        return 0.0

    # Calculate a(x)
    intra_points = X[intra_mask]
    a_x = float(np.mean(np.sqrt(np.sum((intra_points - query_point) ** 2, axis=1))))

    # 2. Calculate b(x): find the minimum mean distance to all other clusters
    unique_labels = np.unique(labels)
    b_x = float("inf")

    for label in unique_labels:
        if label == query_label:
            continue

        # Get points belonging to neighbor cluster
        neighbor_mask = (labels == label)
        neighbor_points = X[neighbor_mask]

        # Compute mean distance to this cluster
        mean_dist_to_cluster = np.mean(np.sqrt(np.sum((neighbor_points - query_point) ** 2, axis=1)))
        b_x = min(b_x, float(mean_dist_to_cluster))

    # Handle single point clusters or edge cases
    if b_x == float("inf"):
        return 0.0

    # Calculate silhouette coefficient
    denom = max(a_x, b_x)
    if denom == 0.0:
        return 0.0

    return (b_x - a_x) / denom
