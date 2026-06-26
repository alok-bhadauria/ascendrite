import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


class LSTMCellNumPy:
    """Implements a single LSTM cell forward step in NumPy."""

    def __init__(self, in_features: int, hidden_dim: int):
        self.d = in_features
        self.h = hidden_dim

        # Forget gate weights
        self.W_xf = np.random.randn(self.h, self.d) * 0.1
        self.W_hf = np.random.randn(self.h, self.h) * 0.1
        self.b_f = np.ones((self.h, 1))  # Default forget bias initialization to 1.0

        # Input gate weights
        self.W_xi = np.random.randn(self.h, self.d) * 0.1
        self.W_hi = np.random.randn(self.h, self.h) * 0.1
        self.b_i = np.zeros((self.h, 1))

        # Candidate state weights
        self.W_xc = np.random.randn(self.h, self.d) * 0.1
        self.W_hc = np.random.randn(self.h, self.h) * 0.1
        self.b_c = np.zeros((self.h, 1))

        # Output gate weights
        self.W_xo = np.random.randn(self.h, self.d) * 0.1
        self.W_ho = np.random.randn(self.h, self.h) * 0.1
        self.b_o = np.zeros((self.h, 1))

    def forward_step(
        self, x_t: np.ndarray, h_prev: np.ndarray, c_prev: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Computes the forward step of the LSTM cell.

        Args:
            x_t: Input vector of shape (d, N)
            h_prev: Previous hidden state of shape (h, N)
            c_prev: Previous cell state of shape (h, N)

        Returns:
            tuple containing:
                - h_t: New hidden state of shape (h, N)
                - c_t: New cell state of shape (h, N)
        """
        # 1. Compute gates
        f_t = sigmoid(np.dot(self.W_xf, x_t) + np.dot(self.W_hf, h_prev) + self.b_f)
        i_t = sigmoid(np.dot(self.W_xi, x_t) + np.dot(self.W_hi, h_prev) + self.b_i)
        c_cand = np.tanh(np.dot(self.W_xc, x_t) + np.dot(self.W_hc, h_prev) + self.b_c)
        o_t = sigmoid(np.dot(self.W_xo, x_t) + np.dot(self.W_ho, h_prev) + self.b_o)

        # 2. Update Cell State
        c_t = f_t * c_prev + i_t * c_cand

        # 3. Update Hidden State
        h_t = o_t * np.tanh(c_t)

        return h_t, c_t


if __name__ == "__main__":
    print("--- Running LSTM Cell Step Verification ---")
    np.random.seed(42)

    d, h, N = 2, 3, 1
    cell = LSTMCellNumPy(in_features=d, hidden_dim=h)

    x_t = np.random.randn(d, N)
    h_prev = np.random.randn(h, N)
    c_prev = np.random.randn(h, N)

    h_t, c_t = cell.forward_step(x_t, h_prev, c_prev)
    print("New Hidden State:\n", h_t)
    print("New Cell State:\n", c_t)

    assert h_t.shape == (h, N)
    assert c_t.shape == (h, N)

    # Verify forget gate with high bias matches expectation
    # b_f is initialized to 1.0, so f_t should be relatively high
    # Let's verify forget gate value manually
    f_t_val = sigmoid(np.dot(cell.W_xf, x_t) + np.dot(cell.W_hf, h_prev) + cell.b_f)
    print("Forget gate activations:\n", f_t_val)
    assert np.all(f_t_val > 0.5)  # Since b_f = 1.0 and weights are small, f_t should be > 0.5
    print("Forget gate bias initialization effect confirmed.")

    print("\n  [PASS] LSTM cell forward step verified successfully.")
