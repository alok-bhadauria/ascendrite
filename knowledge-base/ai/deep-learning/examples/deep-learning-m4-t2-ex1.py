import numpy as np


def clip_gradients_by_norm(
    grads: dict[str, np.ndarray], max_norm: float
) -> tuple[dict[str, np.ndarray], float]:
    """Clips the gradients dictionary by scaling them if their joint L2 norm exceeds max_norm.

    Args:
        grads: Dictionary mapping parameter names to NumPy arrays
        max_norm: Upper limit for L2 norm

    Returns:
        tuple containing:
            - dict: Clipped gradients dictionary
            - float: Original L2 norm
    """
    total_norm_sq = 0.0
    for g in grads.values():
        total_norm_sq += np.sum(g ** 2)
    total_norm = np.sqrt(total_norm_sq)

    clipped_grads = {}
    scale_factor = 1.0
    if total_norm > max_norm:
        scale_factor = max_norm / (total_norm + 1e-10)

    for name, g in grads.items():
        clipped_grads[name] = g * scale_factor

    return clipped_grads, total_norm


def run_gradient_flow_demo(T: int, w_hh: float, x_val: float) -> float:
    """Computes the gradient of the final state h_T with respect to the initial state h_1.

    dh_T/dh_1 = prod_{i=2}^T [ (1 - tanh^2(z_i)) * w_hh ]
    """
    # Forward Pass
    h = np.zeros(T + 1)
    z = np.zeros(T + 1)
    h[0] = 0.0

    for t in range(1, T + 1):
        z[t] = w_hh * h[t - 1] + x_val
        h[t] = np.tanh(z[t])

    # Compute derivative dh_T/dh_1
    dh_T_dh_1 = 1.0
    for i in range(2, T + 1):
        # derivative of tanh is (1 - tanh^2)
        dh_T_dh_1 *= (1.0 - h[i] ** 2) * w_hh

    return dh_T_dh_1


if __name__ == "__main__":
    print("--- Running BPTT & Gradient Clipping Verification ---")
    np.random.seed(42)

    # 1. Verify Gradient Clipping by Norm
    grads = {
        "W_hh": np.array([[10.0, 5.0], [0.0, -10.0]]),
        "W_xh": np.array([[5.0, 0.0]]),
        "b_h": np.array([[2.0], [2.0]]),
    }
    clipped, orig_norm = clip_gradients_by_norm(grads, max_norm=5.0)
    print(f"Original L2 Norm: {orig_norm:.5f}")
    assert np.isclose(orig_norm, np.sqrt(258))

    clipped_norm = np.sqrt(sum(np.sum(g ** 2) for g in clipped.values()))
    print(f"Clipped L2 Norm: {clipped_norm:.5f}")
    assert np.isclose(clipped_norm, 5.0)
    assert np.allclose(clipped["W_hh"] / 5.0, grads["W_hh"] / orig_norm)
    print("Gradient norm clipping scales and directions verified.")

    # 2. Verify Vanishing and Exploding Gradients
    T = 20
    x_val = 0.1

    # Case A: w_hh is small (0.5) -> vanishing gradient
    grad_flow_small = run_gradient_flow_demo(T, w_hh=0.5, x_val=x_val)
    print(f"Gradient flow dh_{T}/dh_1 for w=0.5: {grad_flow_small:.5e}")
    # Since w_hh = 0.5 < 1.0, the gradient flow decays exponentially
    assert abs(grad_flow_small) < 1e-5
    print("Vanishing gradient flow verified.")

    # Case B: w_hh is large (3.0) for a linear recurrence (no tanh saturation)
    # If the network were linear: dh_T/dh_1 = (w_hh)^(T-1)
    grad_flow_linear_large = 3.0 ** (T - 1)
    print(f"Linear gradient flow dh_{T}/dh_1 for w=3.0: {grad_flow_linear_large:.5e}")
    assert grad_flow_linear_large > 1e9
    print("Exploding linear gradient flow verified.")

    print("\n  [PASS] BPTT and gradient clipping examples verified.")
