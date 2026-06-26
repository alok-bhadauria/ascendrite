import numpy as np


def compute_gru_updates(
    r: np.ndarray,
    z: np.ndarray,
    x_t: np.ndarray,
    h_prev: np.ndarray,
    W_xh: np.ndarray,
    W_hh: np.ndarray,
    b_h: np.ndarray,
) -> np.ndarray:
    """Computes the candidate hidden state and final state of a GRU cell.

    Args:
        r: Reset gate activations of shape (h, N)
        z: Update gate activations of shape (h, N)
        x_t: Input vector of shape (d, N)
        h_prev: Previous hidden state of shape (h, N)
        W_xh: Input-to-candidate weights of shape (h, d)
        W_hh: Hidden-to-candidate weights of shape (h, h)
        b_h: Candidate bias of shape (h, 1)

    Returns:
        np.ndarray: Updated hidden state of shape (h, N)
    """
    # 1. Compute candidate hidden state: tanh(W_xh * x_t + W_hh * (r * h_prev) + b_h)
    gated_history = r * h_prev
    h_cand = np.tanh(np.dot(W_xh, x_t) + np.dot(W_hh, gated_history) + b_h)

    # 2. Linear interpolation update: h_t = (1 - z) * h_prev + z * h_cand
    h_t = (1.0 - z) * h_prev + z * h_cand

    return h_t


if __name__ == "__main__":
    print("--- Running GRU Update Mechanics Practice ---")

    # Dimensions: d=2 (input features), h=3 (hidden dimension), N=1 (batch size)
    x_t = np.array([[1.0], [-1.0]])
    h_prev = np.array([[0.8], [0.5], [-0.4]])

    # Pre-calculated gates
    r = np.array([[0.5], [1.0], [0.0]])
    z = np.array([[0.8], [0.2], [0.9]])

    W_xh = np.array([[0.1, 0.2], [0.3, -0.1], [0.0, 0.4]])
    W_hh = np.array([[0.4, 0.1, -0.2], [-0.1, 0.2, 0.3], [0.5, 0.0, 0.1]])
    b_h = np.array([[0.1], [-0.2], [0.3]])

    # Calculate step manually:
    # gated_history = r * h_prev = [0.5*0.8, 1.0*0.5, 0.0*-0.4] = [0.4, 0.5, 0.0]
    # W_xh * x_t = [0.1*1 + 0.2*-1, 0.3*1 + -0.1*-1, 0 + 0.4*-1] = [-0.1, 0.4, -0.4]
    # W_hh * gated_history = [0.4*0.4 + 0.1*0.5 + 0, -0.1*0.4 + 0.2*0.5 + 0, 0.5*0.4 + 0 + 0]
    #                       = [0.21, 0.06, 0.2]
    # h_cand = tanh( [-0.1 + 0.21 + 0.1, 0.4 + 0.06 - 0.2, -0.4 + 0.2 + 0.3] )
    #        = tanh( [0.21, 0.26, 0.1] )
    #        = [tanh(0.21), tanh(0.26), tanh(0.1)]
    #        = [0.20696956, 0.25425442, 0.09966799]
    #
    # h_t = (1 - z) * h_prev + z * h_cand
    # h_t[0] = 0.2 * 0.8 + 0.8 * tanh(0.21) = 0.16 + 0.8 * 0.20696956 = 0.32557565
    # h_t[1] = 0.8 * 0.5 + 0.2 * tanh(0.26) = 0.40 + 0.2 * 0.25425442 = 0.45085088
    # h_t[2] = 0.1 * -0.4 + 0.9 * tanh(0.1) = -0.04 + 0.9 * 0.09966799 = 0.04970119

    h_t = compute_gru_updates(r, z, x_t, h_prev, W_xh, W_hh, b_h)
    print("Calculated hidden state:\n", h_t)

    expected_h0 = 0.16 + 0.8 * np.tanh(0.21)
    expected_h1 = 0.40 + 0.2 * np.tanh(0.26)
    expected_h2 = -0.04 + 0.9 * np.tanh(0.1)

    assert np.allclose(h_t, np.array([[expected_h0], [expected_h1], [expected_h2]]))
    print("GRU updates match manual calculations.")

    print("\n  [PASS] GRU update practice verified.")
