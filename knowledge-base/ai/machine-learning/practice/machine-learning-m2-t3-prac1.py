import numpy as np


def detect_outliers_mahalanobis(
    data: np.ndarray, threshold: float
) -> np.ndarray:
    """Calculates Mahalanobis distance from scratch for each sample in data

    and returns a boolean array indicating which samples are outliers
    (distance > threshold).

    Ensure:
    1. Base covariance calculation handles matrix layouts correctly.
    2. Uses regularized covariance if data has collinearity.
    """
    n_samples, n_features = data.shape
    mean = np.mean(data, axis=0)
    data_centered = data - mean

    # Covariance matrix calculation
    cov = np.cov(data.T)

    # Add diagonal regularization
    cov_reg = cov + 1e-6 * np.eye(n_features)

    # Invert covariance
    inv_cov = np.linalg.inv(cov_reg)

    # Calculate distances
    distances = np.zeros(n_samples)
    for i in range(n_samples):
        diff = data_centered[i]
        distances[i] = np.sqrt(diff.T @ inv_cov @ diff)

    return distances > threshold
