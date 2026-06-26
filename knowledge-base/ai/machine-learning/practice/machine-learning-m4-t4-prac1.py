import numpy as np


def calculate_oob_mask(
    bootstrap_indices: np.ndarray, n_samples: int
) -> np.ndarray:
    """Generates a boolean mask indicating which samples are Out-of-Bag (OOB) for each estimator.

    Args:
        bootstrap_indices: Integer array of shape (n_estimators, n_samples) containing the
                           in-bag indices sampled for each estimator.
        n_samples: Total number of samples in the original training set.

    Returns:
        np.ndarray: Boolean matrix of shape (n_samples, n_estimators), where
                    matrix[i, j] is True if sample i is Out-of-Bag (excluded) for estimator j.
    """
    n_estimators = bootstrap_indices.shape[0]
    oob_mask = np.ones((n_samples, n_estimators), dtype=bool)

    for estimator_idx in range(n_estimators):
        in_bag_idx = bootstrap_indices[estimator_idx]
        # Mark in-bag samples as False (not OOB)
        oob_mask[in_bag_idx, estimator_idx] = False

    return oob_mask


def compute_ensemble_variance(sigma_sq: float, rho: float, B: int) -> float:
    """Computes the analytical variance of a bagged ensemble prediction.

    Formula:
        Var(Y) = rho * sigma_sq + ((1 - rho) / B) * sigma_sq

    Args:
        sigma_sq: The variance of an individual tree prediction.
        rho: The pairwise correlation between tree predictions (0 <= rho <= 1).
        B: The number of trees (estimators) in the ensemble.

    Returns:
        float: The variance of the ensemble average.
    """
    if B <= 0:
        raise ValueError("Number of estimators B must be positive.")
    if not (0.0 <= rho <= 1.0):
        raise ValueError("Correlation rho must lie within [0, 1].")

    term1 = rho * sigma_sq
    term2 = ((1.0 - rho) / B) * sigma_sq
    return float(term1 + term2)
