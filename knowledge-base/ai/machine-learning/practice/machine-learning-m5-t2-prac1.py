import numpy as np


def compute_explained_variance_ratio(
    eigenvalues: np.ndarray, k: int
) -> float:
    """Computes the cumulative explained variance ratio of the top k principal components.

    Formula:
        Ratio = sum_{i=1}^k lambda_i / sum_{j=1}^d lambda_j

    Args:
        eigenvalues: Sorted array of eigenvalues of the covariance matrix in descending order.
        k: Number of components to evaluate.

    Returns:
        float: Cumulative explained variance ratio.
    """
    if len(eigenvalues) == 0 or k <= 0:
        return 0.0

    total_variance = np.sum(eigenvalues)
    if total_variance == 0.0:
        return 0.0

    k_variance = np.sum(eigenvalues[:k])
    return float(k_variance / total_variance)


def project_data_svd(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Projects raw data X onto its top k principal components using Singular Value Decomposition.

    Ensure:
    1. The input feature matrix is centered column-wise before SVD.
    2. The return is a tuple: (X_projected, eigenvalues_k).

    Args:
        X: Raw feature matrix of shape (n_samples, n_features).
        k: Projection dimension (number of principal components).

    Returns:
        tuple: (X_projected, eigenvalues_k)
            - X_projected: projected matrix of shape (n_samples, k).
            - eigenvalues_k: array of shape (k,) containing eigenvalues of top k components.
    """
    n_samples = X.shape[0]

    # Center the data
    mean_vec = np.mean(X, axis=0)
    X_centered = X - mean_vec

    # SVD: X_centered = U * S * V^T
    _, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

    # Top k components
    S_k = S[:k]
    V_k = Vt.T[:, :k]

    # Project data
    X_projected = X_centered @ V_k

    # Compute eigenvalues: lambda_i = sigma_i^2 / N
    eigenvalues_k = (S_k ** 2) / n_samples

    return X_projected, eigenvalues_k
