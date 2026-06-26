import numpy as np


def calculate_shannon_entropy(y: np.ndarray) -> float:
    """Computes the Shannon Entropy of a label array y.

    Formula:
        Entropy = -sum(p_k * log_2(p_k))
        with 0 * log_2(0) = 0.
    """
    n_samples = len(y)
    if n_samples == 0:
        return 0.0

    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / n_samples

    # Compute entropy, filter out 0 probabilities to prevent log2(0) error
    probabilities = probabilities[probabilities > 0.0]
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return float(entropy)


def calculate_variance_reduction(
    y_parent: np.ndarray, y_left: np.ndarray, y_right: np.ndarray
) -> float:
    """Computes the Variance Reduction achieved by splitting a parent node into left and right children.

    Formula:
        VR = Var(y_parent) - ( (|y_left|/|y_parent|) * Var(y_left) + (|y_right|/|y_parent|) * Var(y_right) )
    """
    n_parent = len(y_parent)
    if n_parent == 0:
        return 0.0

    n_left = len(y_left)
    n_right = len(y_right)

    # Compute variances
    var_parent = np.var(y_parent) if n_parent > 0 else 0.0
    var_left = np.var(y_left) if n_left > 0 else 0.0
    var_right = np.var(y_right) if n_right > 0 else 0.0

    # Weighted child variance
    weighted_child_var = (n_left / n_parent) * var_left + (n_right / n_parent) * var_right

    # Variance Reduction
    variance_reduction = var_parent - weighted_child_var

    return float(variance_reduction)
