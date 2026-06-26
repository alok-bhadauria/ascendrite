import numpy as np


def has_gradient_overflow(grads: dict[str, np.ndarray]) -> bool:
    """Checks if any gradient value in the dictionary contains NaN or Inf.

    Returns:
        bool: True if overflow detected, False otherwise
    """
    for name, g in grads.items():
        if np.any(np.isnan(g)) or np.any(np.isinf(g)):
            return True
    return False


if __name__ == "__main__":
    print("--- Running Gradient Overflow Check Practice ---")

    # Case 1: Clean gradients
    grads_clean = {
        "W1": np.array([[0.1, -0.5], [0.3, 0.0]]),
        "b1": np.array([[0.01], [0.02]]),
    }
    assert not has_gradient_overflow(grads_clean)
    print("Case 1 (Clean) check passed.")

    # Case 2: Contains NaN
    grads_nan = {
        "W1": np.array([[0.1, np.nan], [0.3, 0.0]]),
        "b1": np.array([[0.01], [0.02]]),
    }
    assert has_gradient_overflow(grads_nan)
    print("Case 2 (NaN check) passed.")

    # Case 3: Contains Inf
    grads_inf = {
        "W1": np.array([[0.1, -0.5], [0.3, 0.0]]),
        "b1": np.array([[0.01], [np.inf]]),
    }
    assert has_gradient_overflow(grads_inf)
    print("Case 3 (Inf check) passed.")

    print("\n  [PASS] Gradient overflow checking practice verified.")
