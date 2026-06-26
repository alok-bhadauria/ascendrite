import numpy as np


def compute_conv_output_shape(
    h_in: int,
    w_in: int,
    k_h: int,
    k_w: int,
    padding: int,
    stride: int,
) -> tuple[int, int]:
    """Calculates the output height and width of a 2D convolutional layer.

    Uses the spatial dimension formula:
    out = floor((in - kernel + 2 * padding) / stride) + 1
    """
    h_out = int(np.floor((h_in - k_h + 2 * padding) / stride)) + 1
    w_out = int(np.floor((w_in - k_w + 2 * padding) / stride)) + 1
    return h_out, w_out


if __name__ == "__main__":
    print("--- Running CNN Output Shape Calculation Practice ---")

    # Case 1: Standard same convolution
    h, w = compute_conv_output_shape(
        h_in=224, w_in=224, k_h=3, k_w=3, padding=1, stride=1
    )
    print(f"Case 1 (Same): H={h}, W={w}")
    assert h == 224 and w == 224

    # Case 2: Strided convolution (pooling/downsampling proxy)
    h, w = compute_conv_output_shape(
        h_in=224, w_in=224, k_h=7, k_w=7, padding=3, stride=2
    )
    print(f"Case 2 (Strided): H={h}, W={w}")
    # (224 - 7 + 6)/2 + 1 = 223/2 + 1 = 111.5 + 1 -> floor(111.5) + 1 = 111 + 1 = 112
    assert h == 112 and w == 112

    # Case 3: Valid convolution (no padding)
    h, w = compute_conv_output_shape(
        h_in=28, w_in=28, k_h=5, k_w=5, padding=0, stride=1
    )
    print(f"Case 3 (Valid): H={h}, W={w}")
    # 28 - 5 + 1 = 24
    assert h == 24 and w == 24

    # Case 4: Uneven dimensions and stride mismatch
    h, w = compute_conv_output_shape(
        h_in=10, w_in=15, k_h=3, k_w=5, padding=1, stride=3
    )
    print(f"Case 4 (Uneven): H={h}, W={w}")
    # Height: (10 - 3 + 2)/3 + 1 = 9/3 + 1 = 4
    # Width: (15 - 5 + 2)/3 + 1 = 12/3 + 1 = 5
    assert h == 4 and w == 5

    print("\n  [PASS] Output shape calculation logic verified successfully.")
