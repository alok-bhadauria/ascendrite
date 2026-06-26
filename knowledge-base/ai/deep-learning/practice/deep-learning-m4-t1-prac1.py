import numpy as np


def rnn_step_forward(
    x_t: np.ndarray,
    h_prev: np.ndarray,
    W_xh: np.ndarray,
    W_hh: np.ndarray,
    b_h: np.ndarray,
) -> np.ndarray:
    """Computes the hidden state update for a single time step of an RNN.

    Args:
        x_t: Input vector at current step of shape (d, N)
        h_prev: Previous hidden state of shape (h, N)
        W_xh: Input-to-hidden weights of shape (h, d)
        W_hh: Hidden-to-hidden recurrent weights of shape (h, h)
        b_h: Bias vector of shape (h, 1)

    Returns:
        np.ndarray: Updated hidden state of shape (h, N)
    """
    # h_t = tanh(W_hh * h_prev + W_xh * x_t + b_h)
    z = np.dot(W_hh, h_prev) + np.dot(W_xh, x_t) + b_h
    h_t = np.tanh(z)
    return h_t


if __name__ == "__main__":
    print("--- Running RNN Step Forward Practice ---")

    # Dimensions: d=2 (features), h=3 (hidden dim), N=1 (batch size)
    x_t = np.array([[1.0], [-1.0]])
    h_prev = np.array([[0.5], [0.0], [-0.5]])

    W_xh = np.array([[0.1, -0.2], [0.3, 0.0], [-0.1, 0.5]])
    W_hh = np.array([[0.5, 0.1, -0.1], [0.0, 0.2, 0.4], [0.1, -0.3, 0.2]])
    b_h = np.array([[0.1], [-0.1], [0.2]])

    # Calculate step manually:
    # W_xh * x_t = [0.1*1 + -0.2*-1, 0.3*1 + 0, -0.1*1 + 0.5*-1] = [0.3, 0.3, -0.6]
    # W_hh * h_prev = [0.5*0.5 + 0.1*0 + -0.1*-0.5, 0 + 0 + 0.4*-0.5, 0.1*0.5 + 0 + 0.2*-0.5]
    #               = [0.3, -0.2, -0.05]
    # z = [0.3 + 0.3 + 0.1, -0.2 + 0.3 - 0.1, -0.05 - 0.6 + 0.2] = [0.7, 0.0, -0.45]
    # h_t = tanh(z) = [tanh(0.7), tanh(0.0), tanh(-0.45)]
    #               = [0.60436777, 0.0, -0.42189901]
    h_t = rnn_step_forward(x_t, h_prev, W_xh, W_hh, b_h)
    print("Calculated hidden state:\n", h_t)

    expected = np.array(
        [[np.tanh(0.7)],
         [np.tanh(0.0)],
         [np.tanh(-0.45)]]
    )
    assert np.allclose(h_t, expected)
    print("RNN step transition matches manual calculation.")

    print("\n  [PASS] RNN step forward practice verified.")
