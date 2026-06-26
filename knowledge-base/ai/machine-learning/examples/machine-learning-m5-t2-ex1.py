import numpy as np


def pca_via_eigendecomposition(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Computes PCA of X using explicit empirical covariance matrix Eigendecomposition.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        k: Number of principal components to project onto.

    Returns:
        tuple: (X_projected, eigenvectors, eigenvalues)
    """
    n_samples = X.shape[0]

    # 1. Zero-mean center the data column-wise
    mean_vector = np.mean(X, axis=0)
    X_centered = X - mean_vector

    # 2. Compute empirical covariance matrix: (1/N) * X^T * X
    covariance_matrix = (X_centered.T @ X_centered) / n_samples

    # 3. Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Sort eigenvalues and eigenvectors in descending order
    sorted_idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_idx]
    eigenvectors = eigenvectors[:, sorted_idx]

    # Select top k components
    eigenvectors_k = eigenvectors[:, :k]
    eigenvalues_k = eigenvalues[:k]

    # Project data: X_centered * V_k
    X_projected = X_centered @ eigenvectors_k

    return X_projected, eigenvectors_k, eigenvalues_k


def pca_via_svd(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Computes PCA of X directly using Singular Value Decomposition (SVD).

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        k: Number of principal components to project onto.

    Returns:
        tuple: (X_projected, right_singular_vectors, corresponding_eigenvalues)
    """
    n_samples = X.shape[0]

    # 1. Zero-mean center the data
    mean_vector = np.mean(X, axis=0)
    X_centered = X - mean_vector

    # 2. Perform SVD: X = U * S * V^T
    # full_matrices=False computes economy SVD
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

    # Singular values in S are already sorted in descending order.
    # The right singular vectors are the rows of Vt, i.e., columns of V.
    V = Vt.T

    # Select top k components
    V_k = V[:, :k]
    S_k = S[:k]

    # Project data: U_k * S_k = X_centered * V_k
    X_projected = X_centered @ V_k

    # Calculate corresponding covariance eigenvalues: lambda_i = sigma_i^2 / N
    eigenvalues_k = (S_k ** 2) / n_samples

    return X_projected, V_k, eigenvalues_k


if __name__ == "__main__":
    # Generate random high-dimensional dataset
    np.random.seed(42)
    n_samples = 100
    n_features = 5
    X_data = np.random.randn(n_samples, n_features)
    # Inject linear correlations
    X_data[:, 1] = X_data[:, 0] * 2.5 + np.random.normal(0, 0.2, n_samples)
    X_data[:, 3] = X_data[:, 2] * -1.5 + np.random.normal(0, 0.2, n_samples)

    k_components = 2

    # Run both PCA formulations
    X_proj_eig, V_eig, lambda_eig = pca_via_eigendecomposition(X_data, k_components)
    X_proj_svd, V_svd, lambda_svd = pca_via_svd(X_data, k_components)

    print("PCA Eigendecomposition vs SVD Equivalence:")
    print("-" * 50)
    print("Eigenvalues (Eigendecomposition):", lambda_eig)
    print("Eigenvalues (SVD formulation):   ", lambda_svd)
    print("Eigenvalues absolute diff:       ", np.abs(lambda_eig - lambda_svd))

    # Compare eigenvectors/right singular vectors (up to sign flips)
    # We take absolute value to align sign directions
    vector_diff = np.abs(np.abs(V_eig) - np.abs(V_svd))
    projection_diff = np.abs(np.abs(X_proj_eig) - np.abs(X_proj_svd))

    print("\nMax absolute difference in projection vectors: ", np.max(vector_diff))
    print("Max absolute difference in projected coordinates:", np.max(projection_diff))
