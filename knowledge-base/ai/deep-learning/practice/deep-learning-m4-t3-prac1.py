import numpy as np


def compute_lstm_updates(
    f: np.ndarray,
    i: np.ndarray,
    c_cand: np.ndarray,
    o: np.ndarray,
    c_prev: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Computes the cell state and hidden state updates of an LSTM cell.

    Args:
        f: Forget gate activations of shape (h, N)
        i: Input gate activations of shape (h, N)
        c_cand: Candidate cell values of shape (h, N)
        o: Output gate activations of shape (h, N)
        c_prev: Previous cell state of shape (h, N)

    Returns:
        tuple containing:
            - c_t: Updated cell state of shape (h, N)
            - h_t: Updated hidden state of shape (h, N)
    """
    # 1. Update cell state: c_t = f * c_prev + i * c_cand
    c_t = f * c_prev + i * c_cand

    # 2. Update hidden state: h_t = o * tanh(c_t)
    h_t = o * np.tanh(c_t)

    return c_t, h_t


if __name__ == "__main__":
    print("--- Running LSTM Update Mechanics Practice ---")

    # Mock gate values (h=3, N=1)
    f = np.array([[0.9], [0.8], [0.1]])
    i = np.array([[0.2], [0.5], [0.8]])
    c_cand = np.array([[0.5], [1.0], [-0.5]])
    o = np.array([[0.8], [0.9], [0.5]])

    c_prev = np.array([[1.0], [2.0], [0.0]])

    c_t, h_t = compute_lstm_updates(f, i, c_cand, o, c_prev)

    print("Calculated c_t:\n", c_t)
    print("Calculated h_t:\n", h_t)

    # Manual checks:
    # c_t[0] = 0.9 * 1.0 + 0.2 * 0.5 = 0.9 + 0.1 = 1.0
    # h_t[0] = 0.8 * tanh(1.0) = 0.8 * 0.76159416 = 0.60927533
    expected_c0 = 1.0
    expected_h0 = 0.8 * np.tanh(1.0)

    # c_t[1] = 0.8 * 2.0 + 0.5 * 1.0 = 1.6 + 0.5 = 2.1
    # h_t[1] = 0.9 * tanh(2.1) = 0.9 * 0.97045194 = 0.87340674
    expected_c1 = 2.1
    expected_h1 = 0.9 * np.tanh(2.1)

    # c_t[2] = 0.1 * 0.0 + 0.8 * -0.5 = -0.4
    # h_t[2] = 0.5 * tanh(-0.4) = 0.5 * -0.37994896 = -0.18997448
    expected_c2 = -0.4
    expected_h2 = 0.5 * np.tanh(-0.4)

    assert np.allclose(c_t, np.array([[expected_c0], [expected_c1], [expected_c2]]))
    assert np.allclose(h_t, np.array([[expected_h0], [expected_h1], [expected_h2]]))
    print("LSTM update mathematics verified successfully.")

    print("\n  [PASS] LSTM update practice verified.")
