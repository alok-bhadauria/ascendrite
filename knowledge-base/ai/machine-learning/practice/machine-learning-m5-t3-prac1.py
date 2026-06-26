import numpy as np


def compute_c_factor(n: int) -> float:
    """Computes the average path length of an unsuccessful search in a Binary Search Tree (BST) of size n.

    Formula:
        c(n) = 2 * (ln(n - 1) + Euler_constant) - (2 * (n - 1) / n)
        Euler_constant = 0.5772156649

    Args:
        n: The number of samples (subsample size).

    Returns:
        float: Normalized average path length. Returns 0.0 if n <= 1, and 1.0 if n == 2.
    """
    if n <= 1:
        return 0.0
    if n == 2:
        return 1.0

    euler_constant = 0.5772156649
    harmonic_approx = np.log(n - 1) + euler_constant
    adjustment = 2.0 * (n - 1) / n

    return float(2.0 * harmonic_approx - adjustment)


def compute_anomaly_score(
    expected_path_length: np.ndarray, n_subsample: int
) -> np.ndarray:
    """Computes the Isolation Forest anomaly score for given expected path lengths.

    Formula:
        s(x, n) = 2^(-E[h(x)] / c(n))

    Args:
        expected_path_length: NumPy array of expected path lengths E[h(x)] for observations.
        n_subsample: Subsample size used during tree fitting.

    Returns:
        np.ndarray: Computed anomaly scores in range [0, 1].
    """
    c_n = compute_c_factor(n_subsample)

    if c_n == 0.0:
        return np.zeros_like(expected_path_length, dtype=float)

    scores = 2.0 ** (-expected_path_length / c_n)
    return scores
