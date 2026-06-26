import numpy as np


def layer_normalization(
    X: np.ndarray, gamma: np.ndarray, beta: np.ndarray, eps: float = 1e-5
) -> np.ndarray:
    """Computes the forward pass of Layer Normalization.

    Unlike BatchNorm, statistics are computed across the feature dimensions
    independently for each sample.

    Args:
        X: Input tensor of shape (B, D) where B is batch size and D is features.
        gamma: Scale parameter of shape (1, D).
        beta: Shift parameter of shape (1, D).
        eps: Small constant for numerical stability.

    Returns:
        np.ndarray: Normalized and shifted outputs of shape (B, D).
    """
    # 1. Compute mean across the feature dimension (axis=1)
    mean = np.mean(X, axis=1, keepdims=True)  # Shape (B, 1)

    # 2. Compute variance across the feature dimension (axis=1)
    var = np.mean((X - mean) ** 2, axis=1, keepdims=True)  # Shape (B, 1)

    # 3. Normalize activations
    X_hat = (X - mean) / np.sqrt(var + eps)  # Shape (B, D)

    # 4. Affine scale and shift
    out = gamma * X_hat + beta  # Shape (B, D)

    return out


if __name__ == "__main__":
    print("--- Running Layer Normalization Forward Practice ---")

    # Input batch of size 2, feature dimension 3
    X = np.array([[1.0, 2.0, 3.0], [-10.0, 0.0, 10.0]])
    gamma = np.ones((1, 3))
    beta = np.zeros((1, 3))

    out = layer_normalization(X, gamma, beta)
    print("LayerNorm Output:\n", out)

    # For row 1: [1.0, 2.0, 3.0]
    # mean = 2.0, var = ((1-2)^2 + (2-2)^2 + (3-2)^2)/3 = 2/3 = 0.666667
    # std = sqrt(2/3) = 0.816497
    # normalized: [(1-2)/std, (2-2)/std, (3-2)/std] = [-1.22474487, 0.0, 1.22474487]

    expected_row1 = np.array([-1.22474487, 0.0, 1.22474487])
    assert np.allclose(out[0], expected_row1, atol=1e-4)

    # Check that the mean of each row of X_hat (normalized output since gamma=1, beta=0) is exactly zero
    row_means = np.mean(out, axis=1)
    print("Row means of normalized output:", row_means)
    assert np.allclose(row_means, 0.0)

    # Check that the variance of each row of X_hat is exactly one (within tolerance for eps)
    row_vars = np.var(out, axis=1)
    print("Row variances of normalized output:", row_vars)
    assert np.allclose(row_vars, 1.0, atol=1e-4)

    print("\n  [PASS] Layer Normalization forward pass and shape constraints verified.")
