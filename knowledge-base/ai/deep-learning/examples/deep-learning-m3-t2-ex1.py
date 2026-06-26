import numpy as np


def max_pooling_forward(
    X: np.ndarray, kh: int, kw: int, stride: int
) -> tuple[np.ndarray, dict]:
    """Computes the forward pass of 2D Max Pooling.

    Args:
        X: Input tensor of shape (C, H_in, W_in)
        kh: Kernel height
        kw: Kernel width
        stride: Stride size

    Returns:
        tuple containing:
            - np.ndarray: Output tensor of shape (C, H_out, W_out)
            - dict: Cache containing inputs and argmax locations for backward pass
    """
    C, H_in, W_in = X.shape
    H_out = (H_in - kh) // stride + 1
    W_out = (W_in - kw) // stride + 1

    out = np.zeros((C, H_out, W_out))
    # Cache mapping output coordinates to corresponding input argmax coordinates
    argmax_cache = {}

    for c in range(C):
        for h in range(H_out):
            for w in range(W_out):
                h_start = h * stride
                h_end = h_start + kh
                w_start = w * stride
                w_end = w_start + kw

                patch = X[c, h_start:h_end, w_start:w_end]
                out[c, h, w] = np.max(patch)

                # Find the flat index of the max value inside the local patch
                flat_idx = np.argmax(patch)
                # Convert flat patch index to local 2D coordinates
                local_h = flat_idx // kw
                local_w = flat_idx % kw
                # Store absolute coordinates in input X
                argmax_cache[(c, h, w)] = (h_start + local_h, w_start + local_w)

    cache = {"X_shape": X.shape, "argmax_cache": argmax_cache}
    return out, cache


def max_pooling_backward(dY: np.ndarray, cache: dict) -> np.ndarray:
    """Computes the backward pass of 2D Max Pooling.

    Args:
        dY: Output gradients of shape (C, H_out, W_out)
        cache: Cache dictionary from max_pooling_forward

    Returns:
        np.ndarray: Input gradients of shape (C, H_in, W_in)
    """
    X_shape = cache["X_shape"]
    argmax_cache = cache["argmax_cache"]
    dX = np.zeros(X_shape)

    C, H_out, W_out = dY.shape

    for c in range(C):
        for h in range(H_out):
            for w in range(W_out):
                # Retrieve the coordinate of the input element that was the maximum
                in_h, in_w = argmax_cache[(c, h, w)]
                # Route the gradient to that coordinate
                dX[c, in_h, in_w] += dY[c, h, w]

    return dX


def average_pooling_forward(
    X: np.ndarray, kh: int, kw: int, stride: int
) -> tuple[np.ndarray, dict]:
    """Computes the forward pass of 2D Average Pooling.

    Args:
        X: Input tensor of shape (C, H_in, W_in)
        kh: Kernel height
        kw: Kernel width
        stride: Stride size

    Returns:
        tuple containing:
            - np.ndarray: Output tensor of shape (C, H_out, W_out)
            - dict: Cache containing inputs and configuration for backward pass
    """
    C, H_in, W_in = X.shape
    H_out = (H_in - kh) // stride + 1
    W_out = (W_in - kw) // stride + 1

    out = np.zeros((C, H_out, W_out))

    for c in range(C):
        for h in range(H_out):
            for w in range(W_out):
                h_start = h * stride
                h_end = h_start + kh
                w_start = w * stride
                w_end = w_start + kw

                patch = X[c, h_start:h_end, w_start:w_end]
                out[c, h, w] = np.mean(patch)

    cache = {"X_shape": X.shape, "kh": kh, "kw": kw, "stride": stride}
    return out, cache


def average_pooling_backward(dY: np.ndarray, cache: dict) -> np.ndarray:
    """Computes the backward pass of 2D Average Pooling.

    Args:
        dY: Output gradients of shape (C, H_out, W_out)
        cache: Cache dictionary from average_pooling_forward

    Returns:
        np.ndarray: Input gradients of shape (C, H_in, W_in)
    """
    X_shape = cache["X_shape"]
    kh = cache["kh"]
    kw = cache["kw"]
    stride = cache["stride"]

    dX = np.zeros(X_shape)
    C, H_out, W_out = dY.shape
    patch_size = kh * kw

    for c in range(C):
        for h in range(H_out):
            for w in range(W_out):
                h_start = h * stride
                h_end = h_start + kh
                w_start = w * stride
                w_end = w_start + kw

                # Distribute the gradient equally to all inputs in the patch
                dX[c, h_start:h_end, w_start:w_end] += dY[c, h, w] / patch_size

    return dX


if __name__ == "__main__":
    print("--- Running Pooling Operations Verification ---")

    # Define a simple 1-channel 4x4 input
    X = np.array(
        [[[1.0, 3.0, 2.0, 1.0],
          [4.0, 2.0, 1.0, 5.0],
          [3.0, 0.0, 6.0, 2.0],
          [1.0, 4.0, 3.0, 2.0]]]
    )

    # 1. Max Pooling Forward/Backward check
    out_max, cache_max = max_pooling_forward(X, kh=2, kw=2, stride=2)
    expected_max = np.array([[[4.0, 5.0], [4.0, 6.0]]])
    assert np.allclose(out_max, expected_max)
    print("Max pooling forward output matches expected values.")

    dY = np.array([[[1.0, 2.0], [3.0, 4.0]]])
    dX_max = max_pooling_backward(dY, cache_max)
    expected_dX_max = np.zeros_like(X)
    expected_dX_max[0, 1, 0] = 1.0
    expected_dX_max[0, 1, 3] = 2.0
    expected_dX_max[0, 3, 1] = 3.0
    expected_dX_max[0, 2, 2] = 4.0
    assert np.allclose(dX_max, expected_dX_max)
    print("Max pooling backward gradients (routing) match expected values.")

    # 2. Average Pooling Forward/Backward check
    out_avg, cache_avg = average_pooling_forward(X, kh=2, kw=2, stride=2)
    expected_avg = np.array([[[2.5, 2.25], [2.0, 3.25]]])
    assert np.allclose(out_avg, expected_avg)
    print("Average pooling forward output matches expected values.")

    dX_avg = average_pooling_backward(dY, cache_avg)
    expected_dX_avg = np.array(
        [[[0.25, 0.25, 0.5, 0.5],
          [0.25, 0.25, 0.5, 0.5],
          [0.75, 0.75, 1.0, 1.0],
          [0.75, 0.75, 1.0, 1.0]]]
    )
    assert np.allclose(dX_avg, expected_dX_avg)
    print("Average pooling backward gradients match expected values.")

    print("\n  [PASS] Pooling examples verified successfully.")
