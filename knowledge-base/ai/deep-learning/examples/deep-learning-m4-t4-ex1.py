import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


class GRUCellNumPy:
    """Implements a single GRU cell forward step in NumPy."""

    def __init__(self, in_features: int, hidden_dim: int):
        self.d = in_features
        self.h = hidden_dim

        # Reset gate weights
        self.W_xr = np.random.randn(self.h, self.d) * 0.1
        self.W_hr = np.random.randn(self.h, self.h) * 0.1
        self.b_r = np.zeros((self.h, 1))

        # Update gate weights
        self.W_xz = np.random.randn(self.h, self.d) * 0.1
        self.W_hz = np.random.randn(self.h, self.h) * 0.1
        self.b_z = np.zeros((self.h, 1))

        # Candidate state weights
        self.W_xh = np.random.randn(self.h, self.d) * 0.1
        self.W_hh = np.random.randn(self.h, self.h) * 0.1
        self.b_h = np.zeros((self.h, 1))

    def forward_step(self, x_t: np.ndarray, h_prev: np.ndarray) -> np.ndarray:
        """Computes the forward step of the GRU cell.

        Args:
            x_t: Input vector of shape (d, N)
            h_prev: Previous hidden state of shape (h, N)

        Returns:
            np.ndarray: New hidden state of shape (h, N)
        """
        # 1. Reset gate
        r_t = sigmoid(np.dot(self.W_xr, x_t) + np.dot(self.W_hr, h_prev) + self.b_r)

        # 2. Update gate
        z_t = sigmoid(np.dot(self.W_xz, x_t) + np.dot(self.W_hz, h_prev) + self.b_z)

        # 3. Candidate hidden state
        # Note: reset gate modulates history BEFORE multiplying by W_hh
        h_cand = np.tanh(
            np.dot(self.W_xh, x_t) + np.dot(self.W_hh, (r_t * h_prev)) + self.b_h
        )

        # 4. Hidden state update (linear interpolation)
        h_t = (1.0 - z_t) * h_prev + z_t * h_cand

        return h_t


if __name__ == "__main__":
    print("--- Running GRU Cell Step Verification ---")
    np.random.seed(42)

    d, h, N = 2, 3, 1
    cell = GRUCellNumPy(in_features=d, hidden_dim=h)

    x_t = np.random.randn(d, N)
    h_prev = np.random.randn(h, N)

    h_t = cell.forward_step(x_t, h_prev)
    print("New Hidden State:\n", h_t)

    assert h_t.shape == (h, N)

    # Prove reset gate behavior:
    # If reset gate is forced to 0, history is ignored
    cell.b_r.fill(-100.0)  # Forces r_t to 0.0
    h_t_reset = cell.forward_step(x_t, h_prev)
    
    # Calculate candidate state with zero history
    r_t_forced = 0.0
    h_cand_expected = np.tanh(np.dot(cell.W_xh, x_t) + cell.b_h)
    z_t_val = sigmoid(np.dot(cell.W_xz, x_t) + np.dot(cell.W_hz, h_prev) + cell.b_z)
    h_t_expected = (1.0 - z_t_val) * h_prev + z_t_val * h_cand_expected

    assert np.allclose(h_t_reset, h_t_expected)
    print("Reset gate modulation verified (history successfully ignored when r_t = 0).")

    print("\n  [PASS] GRU cell forward step verified successfully.")
