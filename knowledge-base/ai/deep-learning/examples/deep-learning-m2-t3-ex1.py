import numpy as np


def soft_thresholding(w: np.ndarray, threshold: float) -> np.ndarray:
    """Applies the soft-thresholding operator (mathematical update for L1).

    sgn(w) * max(0, |w| - threshold)
    """
    return np.sign(w) * np.maximum(0.0, np.abs(w) - threshold)


def dropout_forward(
    x: np.ndarray, p: float, training: bool
) -> tuple[np.ndarray, np.ndarray]:
    """Computes Inverted Dropout forward pass.

    Args:
        x: Input activations tensor of arbitrary shape.
        p: Dropout probability (fraction of units to drop).
        training: True if in training phase, False if inference.

    Returns:
        tuple (out, mask)
    """
    if training and p > 0.0:
        # Bernoulli mask with keep probability 1-p
        mask = (np.random.rand(*x.shape) >= p).astype(float)
        # Scale active elements by 1/(1-p)
        out = (x * mask) / (1.0 - p)
    else:
        out = x
        mask = np.ones_like(x)
    return out, mask


def dropout_backward(
    grad_output: np.ndarray, mask: np.ndarray, p: float
) -> np.ndarray:
    """Computes Inverted Dropout backward pass."""
    return (grad_output * mask) / (1.0 - p)


if __name__ == "__main__":
    print("--- Regularization Mechanics Demo (L1, L2, Dropout) ---")

    # 1. Verify L1 Soft-Thresholding vs L2 Decay
    # We initialize a weight vector with some small values
    np.random.seed(42)
    w_initial = np.array([[1.0], [0.05], [-0.03], [0.8]])
    print("\nInitial Weights:\n", w_initial.tolist())

    eta = 0.1
    lam = 0.4
    threshold = eta * lam  # 0.04

    # Apply L1 Soft-Thresholding step (gradient of L0 is assumed zero for demonstration)
    w_l1 = soft_thresholding(w_initial, threshold)
    print("After L1 Soft-Thresholding step:\n", w_l1.tolist())
    # Values originally at 0.05 and -0.03 are within threshold (0.04), so they should shrink to 0.01 and 0.0 respectively
    # Wait, |0.05| - 0.04 = 0.01 -> sign(0.05)*0.01 = 0.01
    # |-0.03| - 0.04 = -0.01 -> max(0, -0.01) = 0.0 -> sign(-0.03)*0 = 0.0
    assert w_l1[2, 0] == 0.0, "L1 should drive small weights to exactly zero!"

    # Apply L2 Weight Decay step
    w_l2 = w_initial * (1.0 - eta * lam)
    print("After L2 Weight Decay step:\n", w_l2.tolist())
    # Small weights shrink but remain non-zero
    assert (
        w_l2[2, 0] != 0.0
    ), "L2 should not drive small weights to exactly zero!"
    print("  [PASS] L1 soft-thresholding and L2 weight decay verified.")

    # 2. Verify Inverted Dropout Expectation
    # We create a large activation matrix to check the mean scale
    x_large = np.ones((1000, 1000))
    p = 0.3  # drop 30% of neurons

    # Forward training pass
    out_train, mask = dropout_forward(x_large, p=p, training=True)
    mean_train = np.mean(out_train)

    # Forward inference pass
    out_test, _ = dropout_forward(x_large, p=p, training=False)
    mean_test = np.mean(out_test)

    print(f"\nInverted Dropout Expectation (p = {p}):")
    print(f"  Training Activation Mean:  {mean_train:.6f}")
    print(f"  Inference Activation Mean: {mean_test:.6f}")

    # Expectation should be close to 1.0 in both cases due to Inverted Dropout scaling
    assert np.isclose(
        mean_train, 1.0, atol=1e-2
    ), "Inverted Dropout forward scaling failed to preserve expectation!"
    print("  [PASS] Inverted Dropout expectation normalization verified.")

    # 3. Verify Dropout Backward Pass scaling
    grad_out = np.ones((5, 5))
    _, mask_small = dropout_forward(np.ones((5, 5)), p=0.4, training=True)
    grad_in = dropout_backward(grad_out, mask_small, p=0.4)

    # Gradients for active elements must be scaled by 1/(1-p) = 1/0.6 = 1.6666...
    # Gradients for dropped elements must be exactly zero
    for r in range(5):
        for c in range(5):
            if mask_small[r, c] == 1.0:
                assert np.isclose(grad_in[r, c], 1.66666667)
            else:
                assert grad_in[r, c] == 0.0
    print("  [PASS] Inverted Dropout backward gradient scaling verified.")

    print("\nAll regularization mechanics checks passed successfully!")
