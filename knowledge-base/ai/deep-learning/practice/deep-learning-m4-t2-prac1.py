import numpy as np


def clip_by_norm_practice(grad: np.ndarray, max_norm: float) -> np.ndarray:
    """Clips the gradients of a single tensor by its L2 norm.

    If L2 norm is <= max_norm, return grad unchanged.
    If L2 norm is > max_norm, scale grad down.
    """
    # Compute L2 norm of the gradient tensor
    norm = np.sqrt(np.sum(grad ** 2))

    if norm > max_norm:
        # Scale the gradient down to match max_norm
        grad = grad * (max_norm / (norm + 1e-10))

    return grad


if __name__ == "__main__":
    print("--- Running Gradient Clipping Practice ---")

    # Case 1: Norm is below threshold (should remain unchanged)
    g1 = np.array([3.0, 4.0])  # Norm = sqrt(9+16) = 5.0
    g1_clipped = clip_by_norm_practice(g1, max_norm=10.0)
    print("Case 1 (Below threshold) norm:", np.sqrt(np.sum(g1_clipped ** 2)))
    assert np.allclose(g1_clipped, g1)

    # Case 2: Norm is above threshold (should be scaled down)
    g2 = np.array([6.0, 8.0])  # Norm = sqrt(36+64) = 10.0
    g2_clipped = clip_by_norm_practice(g2, max_norm=5.0)
    g2_norm = np.sqrt(np.sum(g2_clipped ** 2))
    print("Case 2 (Above threshold) norm:", g2_norm)
    assert np.isclose(g2_norm, 5.0)
    # Direction check: g2_clipped should be exactly half of g2
    assert np.allclose(g2_clipped, np.array([3.0, 4.0]))

    print("\n  [PASS] Gradient norm clipping practice verified.")
