import numpy as np


def project_and_add(
    F_out: np.ndarray, X: np.ndarray, W_proj: np.ndarray | None
) -> np.ndarray:
    """Combines a residual output and a shortcut input, applying projection if needed.

    Args:
        F_out: Residual block output of shape (C_out, N)
        X: Original block input of shape (C_in, N)
        W_proj: Projection matrix of shape (C_out, C_in) or None (for identity)

    Returns:
        np.ndarray: Combined output of shape (C_out, N)
    """
    if W_proj is not None:
        # Project X to align channels with F_out
        shortcut = np.dot(W_proj, X)
    else:
        # Identity mapping
        shortcut = X

    # Ensure shape alignment
    assert F_out.shape == shortcut.shape, (
        f"Shape mismatch: residual output is {F_out.shape}, "
        f"but shortcut is {shortcut.shape}"
    )

    return F_out + shortcut


if __name__ == "__main__":
    print("--- Running ResNet Projection Practice ---")

    # Case 1: Identity Shortcut (Dimensions already match)
    F_out_1 = np.ones((4, 3)) * 2.0
    X_1 = np.ones((4, 3)) * 0.5
    y_1 = project_and_add(F_out_1, X_1, W_proj=None)
    print("Case 1 (Identity) output shape:", y_1.shape)
    assert np.allclose(y_1, 2.5)

    # Case 2: Projection Shortcut (Dimension mismatch)
    F_out_2 = np.ones((8, 3)) * 1.5
    X_2 = np.ones((4, 3)) * 1.0
    # W_proj of shape (8, 4) to map channels from 4 to 8
    W_proj = np.ones((8, 4)) * 0.25

    y_2 = project_and_add(F_out_2, X_2, W_proj=W_proj)
    print("Case 2 (Projection) output shape:", y_2.shape)
    # W_proj * X_2 will be 4 * (0.25 * 1.0) = 1.0 for each row in output
    # y = F_out + shortcut = 1.5 + 1.0 = 2.5
    assert y_2.shape == (8, 3)
    assert np.allclose(y_2, 2.5)

    print("\n  [PASS] Projection practice verified successfully.")
