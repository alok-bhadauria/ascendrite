import numpy as np


def flatten_forward(X: np.ndarray) -> tuple[np.ndarray, tuple]:
    """Flattens a multi-dimensional feature map tensor.

    Args:
        X: Input feature tensor of shape (C, H, W)

    Returns:
        tuple containing:
            - np.ndarray: Flattened 2D vector of shape (C * H * W, 1)
            - tuple: Original shape of the input tensor (C, H, W)
    """
    original_shape = X.shape
    C, H, W = original_shape
    # Reshape X to a column vector of shape (C * H * W, 1)
    out = X.reshape(C * H * W, 1)
    return out, original_shape


def flatten_backward(dY: np.ndarray, original_shape: tuple) -> np.ndarray:
    """Restores the original multi-dimensional shape for backward gradient flow.

    Args:
        dY: Output gradients of shape (C * H * W, 1)
        original_shape: Original tensor shape (C, H, W)

    Returns:
        np.ndarray: Input gradients reshaped back to (C, H, W)
    """
    # Reshape the flat gradient back to the original 3D tensor shape
    dX = dY.reshape(original_shape)
    return dX


if __name__ == "__main__":
    print("--- Running Flattening Layer Practice ---")

    # Define mock feature map: 3 channels, 2x2 spatial dimension
    X = np.array(
        [[[1.0, 2.0],
          [3.0, 4.0]],
         [[5.0, 6.0],
          [7.0, 8.0]],
         [[9.0, 10.0],
          [11.0, 12.0]]]
    )

    out, orig_shape = flatten_forward(X)
    print("Flattened shape:", out.shape)
    assert out.shape == (12, 1)
    
    # Check flattening mapping order (C-contiguous flattening order: C -> H -> W)
    expected_flat = np.arange(1.0, 13.0).reshape(12, 1)
    assert np.allclose(out, expected_flat)
    print("Flattened mapping values match expected sequence.")

    # Backward gradient pass
    dY = np.ones((12, 1)) * 0.5
    dX = flatten_backward(dY, orig_shape)
    print("Restored shape:", dX.shape)
    assert dX.shape == (3, 2, 2)
    assert np.all(dX == 0.5)
    print("Flattening backward gradients reconstructed successfully.")

    print("\n  [PASS] Flattening layer practice verified.")
