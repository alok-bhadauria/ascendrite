import numpy as np


def adam_step(
    w: np.ndarray,
    g: np.ndarray,
    m: np.ndarray,
    v: np.ndarray,
    t: int,
    lr: float,
    beta1: float,
    beta2: float,
    eps: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Computes a single Adam parameter update step.

    Returns:
        Updated weights w_new, first moment m_new, and second moment v_new.
    """
    # 1. Update biased first moment estimate
    m_new = beta1 * m + (1.0 - beta1) * g

    # 2. Update biased second raw moment estimate
    v_new = beta2 * v + (1.0 - beta2) * (g**2)

    # 3. Compute bias-corrected first moment estimate
    m_hat = m_new / (1.0 - beta1**t)

    # 4. Compute bias-corrected second raw moment estimate
    v_hat = v_new / (1.0 - beta2**t)

    # 5. Update parameters
    w_new = w - (lr / (np.sqrt(v_hat) + eps)) * m_hat

    return w_new, m_new, v_new


if __name__ == "__main__":
    print("--- Running Adam Optimizer Update Step Practice ---")

    # Initialize variables for testing
    w = np.array([[1.0], [-2.0]])
    g = np.array([[0.5], [0.1]])
    m = np.array([[0.0], [0.0]])
    v = np.array([[0.0], [0.0]])

    lr = 0.1
    beta1 = 0.9
    beta2 = 0.999
    eps = 1e-8

    # Perform step 1 (t = 1)
    w, m, v = adam_step(w, g, m, v, 1, lr, beta1, beta2, eps)

    # Calculations for verification:
    # m_new = 0.9 * 0 + 0.1 * g = 0.1 * [[0.5], [0.1]] = [[0.05], [0.01]]
    # v_new = 0.999 * 0 + 0.001 * (g^2) = 0.001 * [[0.25], [0.01]] = [[0.00025], [0.00001]]
    # m_hat = m_new / (1 - 0.9) = [[0.5], [0.1]]
    # v_hat = v_new / (1 - 0.999) = [[0.25], [0.01]]
    # w_new = w - 0.1 * m_hat / (sqrt(v_hat) + eps)
    # w_new = w - 0.1 * [[0.5], [0.1]] / ([[0.5], [0.1]] + 1e-8) = w - [[0.1], [0.1]] = [[0.9], [-2.1]]

    assert np.allclose(m, np.array([[0.05], [0.01]]))
    assert np.allclose(v, np.array([[0.00025], [0.00001]]))
    assert np.allclose(w, np.array([[0.9], [-2.1]]))

    print("  [PASS] Step 1 calculations verified.")

    # Perform step 2 (t = 2)
    w, m, v = adam_step(w, g, m, v, 2, lr, beta1, beta2, eps)

    # Output values printed for check
    print("\nUpdated values at t=2:")
    print("  w:\n", w)
    print("  m:\n", m)
    print("  v:\n", v)

    print("\nAll Adam update step assertions verified successfully!")
