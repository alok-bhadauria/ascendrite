import numpy as np


def compute_optimal_leaf_weight(
    gradients: np.ndarray, hessians: np.ndarray, reg_lambda: float
) -> float:
    """Computes the optimal weight for a terminal leaf node in XGBoost.

    Formula:
        w_j* = -sum(g_i) / (sum(h_i) + lambda)

    Args:
        gradients: NumPy array of first-order gradients of samples in the leaf.
        hessians: NumPy array of second-order gradients of samples in the leaf.
        reg_lambda: L2 regularization parameter lambda.

    Returns:
        float: The optimal leaf weight.
    """
    g_sum = np.sum(gradients)
    h_sum = np.sum(hessians)

    # Avoid division by zero
    denominator = h_sum + reg_lambda
    if denominator <= 0.0:
        return 0.0

    return float(-g_sum / denominator)


def compute_split_gain(
    g_left: np.ndarray,
    h_left: np.ndarray,
    g_right: np.ndarray,
    h_right: np.ndarray,
    reg_lambda: float,
    gamma: float,
) -> float:
    """Computes the split evaluation gain for a candidate split in XGBoost.

    Formula:
        Gain = 0.5 * [ G_L^2 / (H_L + lambda) + G_R^2 / (H_R + lambda) - G_P^2 / (H_P + lambda) ] - gamma
        where G_P = G_L + G_R and H_P = H_L + H_R.

    Args:
        g_left: First-order gradients of samples assigned to the left child.
        h_left: Second-order gradients of samples assigned to the left child.
        g_right: First-order gradients of samples assigned to the right child.
        h_right: Second-order gradients of samples assigned to the right child.
        reg_lambda: L2 regularization parameter lambda.
        gamma: L1 regularization complexity threshold gamma.

    Returns:
        float: The computed split gain.
    """
    # Sums for left child
    G_L = np.sum(g_left)
    H_L = np.sum(h_left)

    # Sums for right child
    G_R = np.sum(g_right)
    H_R = np.sum(h_right)

    # Sums for parent
    G_P = G_L + G_R
    H_P = H_L + H_R

    # Helper helper to calculate score: G^2 / (H + lambda)
    def calc_score(G, H):
        denom = H + reg_lambda
        return (G ** 2) / denom if denom > 0.0 else 0.0

    score_left = calc_score(G_L, H_L)
    score_right = calc_score(G_R, H_R)
    score_parent = calc_score(G_P, H_P)

    # Gain formula
    gain = 0.5 * (score_left + score_right - score_parent) - gamma
    return float(gain)
