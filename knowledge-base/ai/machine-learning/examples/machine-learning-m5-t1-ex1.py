import numpy as np


def kmeans_plus_plus_init(X: np.ndarray, k: int, seed: int = 42) -> np.ndarray:
    """Implements K-Means++ probabilistic centroid initialization.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        k: Number of centroids to initialize.
        seed: Random seed for reproducibility.

    Returns:
        np.ndarray: Initial centroids of shape (k, n_features).
    """
    n_samples, n_features = X.shape
    rng = np.random.default_rng(seed)

    # 1. Choose the first centroid uniformly at random
    centroids = np.zeros((k, n_features))
    first_idx = rng.choice(n_samples)
    centroids[0] = X[first_idx]

    # Initialize distance array
    min_distances = np.full(n_samples, float("inf"))

    for j in range(1, k):
        # 2. Update distance of all points to the nearest already chosen centroid
        newest_centroid = centroids[j - 1]
        distances_to_new = np.sum((X - newest_centroid) ** 2, axis=1)
        min_distances = np.minimum(min_distances, distances_to_new)

        # 3. Select next centroid with probability proportional to D(x)^2
        sum_sq_dist = np.sum(min_distances)
        if sum_sq_dist == 0.0:
            # Fallback if all points coincide with centroids
            probabilities = np.full(n_samples, 1.0 / n_samples)
        else:
            probabilities = min_distances / sum_sq_dist

        next_idx = rng.choice(n_samples, p=probabilities)
        centroids[j] = X[next_idx]

    return centroids


def fit_kmeans(
    X: np.ndarray, k: int, max_iters: int = 100, tol: float = 1e-6
) -> tuple[np.ndarray, np.ndarray, list[float]]:
    """Fits K-Means clustering using Lloyd's coordinate descent algorithm.

    Centroids are initialized using K-Means++.
    """
    n_samples = X.shape[0]

    # 1. Initialize centroids using K-Means++
    centroids = kmeans_plus_plus_init(X, k)
    labels = np.zeros(n_samples, dtype=int)
    wcss_history = []

    for it in range(max_iters):
        # --- Assignment Step ---
        # Compute squared Euclidean distances from all points to all centroids
        # dists shape: (n_samples, k)
        sq_dists = np.sum(X**2, axis=1, keepdims=True) + np.sum(centroids**2, axis=1) - 2 * (X @ centroids.T)
        sq_dists = np.maximum(sq_dists, 0.0)  # Handle minor floating point precision errors

        # Assign each point to the closest centroid
        new_labels = np.argmin(sq_dists, axis=1)

        # Calculate Within-Cluster Sum of Squares (WCSS)
        wcss = float(np.sum(np.min(sq_dists, axis=1)))
        wcss_history.append(wcss)

        # --- Update Step ---
        new_centroids = np.zeros_like(centroids)
        for j in range(k):
            cluster_points = X[new_labels == j]
            if len(cluster_points) > 0:
                new_centroids[j] = np.mean(cluster_points, axis=0)
            else:
                # If a cluster is empty, keep the previous centroid
                new_centroids[j] = centroids[j]

        # Check convergence: stop if centroids do not move significantly
        centroid_shift = np.sum((new_centroids - centroids) ** 2)
        centroids = new_centroids
        labels = new_labels

        print(f"Iteration {it:2d} | WCSS: {wcss:12.5f} | Centroid Shift: {centroid_shift:.8f}")

        if centroid_shift < tol:
            break

    return centroids, labels, wcss_history


if __name__ == "__main__":
    # Generate synthetic isotropic clusters in 2D
    np.random.seed(42)
    cluster1 = np.random.normal(loc=[-2.0, -2.0], scale=0.5, size=(50, 2))
    cluster2 = np.random.normal(loc=[2.0, 2.0], scale=0.5, size=(50, 2))
    cluster3 = np.random.normal(loc=[-2.0, 2.0], scale=0.5, size=(50, 2))
    X_data = np.vstack([cluster1, cluster2, cluster3])

    print("Fitting K-Means Clustering (Pure NumPy):")
    centroids, labels, wcss_hist = fit_kmeans(X_data, k=3)

    print(f"\nFinal WCSS: {wcss_hist[-1]:.5f}")
    print("Centroids:\n", centroids)
