import numpy as np
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer


def perform_mice_imputation(X_miss: np.ndarray) -> np.ndarray:
    """Performs Multivariate Imputation by Chained Equations (MICE)

    using standard iterative ridge regression models.
    """
    imputer = IterativeImputer(max_iter=10, random_state=42)
    return imputer.fit_transform(X_miss)


def compute_mahalanobis_distance(
    X: np.ndarray, regularization: float = 1e-5
) -> np.ndarray:
    """Computes the Mahalanobis distance for each sample in X,

    regularizing the covariance matrix to guarantee invertibility.
    """
    n_samples, n_features = X.shape
    mean = np.mean(X, axis=0)

    # Center the data
    X_centered = X - mean

    # Compute covariance matrix
    covariance = np.cov(X.T)

    # Shrinkage regularization to prevent singularity
    if n_features > 1:
        covariance_reg = covariance + regularization * np.eye(n_features)
    else:
        covariance_reg = np.array([[covariance + regularization]])

    # Invert the covariance matrix
    inv_covariance = np.linalg.inv(covariance_reg)

    # Compute distances: (x - mu).T * Sigma^-1 * (x - mu)
    distances = np.zeros(n_samples)
    for i in range(n_samples):
        diff = X_centered[i]
        distances[i] = np.sqrt(diff.T @ inv_covariance @ diff)

    return distances
