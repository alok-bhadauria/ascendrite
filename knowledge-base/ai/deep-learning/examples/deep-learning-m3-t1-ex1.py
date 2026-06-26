import numpy as np


def conv2d_forward_scratch(
    X: np.ndarray,
    W: np.ndarray,
    b: np.ndarray,
    stride: int = 1,
    padding: int = 0,
) -> np.ndarray:
    """Computes the forward pass of a 2D convolutional layer from scratch.

    Args:
        X: Input tensor of shape (C_in, H_in, W_in)
        W: Weights tensor of shape (C_out, C_in, K_H, K_W)
        b: Bias tensor of shape (C_out, 1)
        stride: Stride step size.
        padding: Padding size added to all sides.

    Returns:
        np.ndarray: Output tensor of shape (C_out, H_out, W_out)
    """
    C_in, H_in, W_in = X.shape
    C_out, C_in_w, K_H, K_W = W.shape

    assert C_in == C_in_w, "Weights input channel dimension must match input!"

    # 1. Compute output dimensions
    H_out = (H_in - K_H + 2 * padding) // stride + 1
    W_out = (W_in - K_W + 2 * padding) // stride + 1

    # 2. Apply Padding
    # Pad only the spatial height and width dimensions (dim 1 and dim 2)
    X_padded = np.pad(
        X,
        pad_width=((0, 0), (padding, padding), (padding, padding)),
        mode="constant",
        constant_values=0.0,
    )

    # 3. Create output tensor
    out = np.zeros((C_out, H_out, W_out))

    # 4. Perform cross-correlation scanning
    for c_o in range(C_out):
        for h in range(H_out):
            for w in range(W_out):
                # Calculate slice coordinates on padded input
                h_start = h * stride
                h_end = h_start + K_H
                w_start = w * stride
                w_end = w_start + K_W

                # Extract the 3D slice of input: shape (C_in, K_H, K_W)
                X_slice = X_padded[:, h_start:h_end, w_start:w_end]

                # Element-wise product and summation over all input channels
                # plus bias
                out[c_o, h, w] = np.sum(X_slice * W[c_o]) + b[c_o, 0]

    return out


if __name__ == "__main__":
    print("--- 2D Convolution Forward Pass Scratch Demo ---")

    # Input: 3 channels (RGB), size 5x5
    np.random.seed(42)
    X = np.random.randn(3, 5, 5)

    # Weights: 2 output channels, 3 input channels, kernel size 3x3
    W = np.random.randn(2, 3, 3, 3)
    b = np.array([[0.5], [-0.2]])

    # Case 1: stride=1, padding=1
    out_1 = conv2d_forward_scratch(X, W, b, stride=1, padding=1)
    print("Output shape (stride=1, padding=1):", out_1.shape)
    # Expected output size: H_out = (5 - 3 + 2)/1 + 1 = 5. Output shape (2, 5, 5)
    assert out_1.shape == (2, 5, 5)

    # Case 2: stride=2, padding=0
    out_2 = conv2d_forward_scratch(X, W, b, stride=2, padding=0)
    print("Output shape (stride=2, padding=0):", out_2.shape)
    # Expected output size: H_out = (5 - 3 + 0)/2 + 1 = 2. Output shape (2, 2, 2)
    assert out_2.shape == (2, 2, 2)

    # Numerical verification on a tiny manual configuration
    X_test = np.array([[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]])  # (1, 3, 3)
    W_test = np.array([[[[1.0, 0.0], [0.0, -1.0]]]])  # (1, 1, 2, 2)
    b_test = np.array([[0.1]])

    out_test = conv2d_forward_scratch(X_test, W_test, b_test, stride=1, padding=0)
    print("\nManual Test Output:\n", out_test)
    # Calculations:
    # H_out = 3 - 2 + 1 = 2
    # Slide 0,0: [[1, 2], [4, 5]] * [[1, 0], [0, -1]] + 0.1 = 1*1 + 5*-1 + 0.1 = -3.9
    # Slide 0,1: [[2, 3], [5, 6]] * [[1, 0], [0, -1]] + 0.1 = 2*1 + 6*-1 + 0.1 = -3.9
    # Slide 1,0: [[4, 5], [7, 8]] * [[1, 0], [0, -1]] + 0.1 = 4*1 + 8*-1 + 0.1 = -3.9
    # Slide 1,1: [[5, 6], [8, 9]] * [[1, 0], [0, -1]] + 0.1 = 5*1 + 9*-1 + 0.1 = -3.9

    expected_out = np.array([[[-3.9, -3.9], [-3.9, -3.9]]])
    assert np.allclose(out_test, expected_out)

    print("\n  [PASS] 2D convolution forward shapes and outputs verified.")
