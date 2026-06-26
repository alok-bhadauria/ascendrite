import numpy as np


class ElmanRNNNumPy:
    """Implements a basic Elman Recurrent Neural Network forward pass in NumPy."""

    def __init__(self, in_features: int, hidden_dim: int):
        self.d = in_features
        self.h = hidden_dim

        # Initialize weights with standard scaling
        self.W_xh = np.random.randn(self.h, self.d) * 0.1
        self.W_hh = np.random.randn(self.h, self.h) * 0.1
        self.b_h = np.zeros((self.h, 1))

    def forward(self, X: np.ndarray, h0: np.ndarray | None = None) -> np.ndarray:
        """Computes forward pass of Elman RNN.

        Args:
            X: Input tensor of shape (d, T, N) where:
                d = input features
                T = sequence length
                N = batch size
            h0: Initial hidden state of shape (h, N). Default is zeros.

        Returns:
            np.ndarray: All hidden states of shape (h, T, N)
        """
        d, T, N = X.shape
        assert d == self.d, "Input feature dimension must match self.d"

        if h0 is None:
            h0 = np.zeros((self.h, N))

        # Store hidden states for all time steps
        H = np.zeros((self.h, T, N))

        h_prev = h0
        for t in range(T):
            x_t = X[:, t, :]  # Shape (d, N)
            
            # Recurrent state transition
            # h_t = tanh(W_hh * h_prev + W_xh * x_t + b_h)
            h_t = np.tanh(
                np.dot(self.W_hh, h_prev) + np.dot(self.W_xh, x_t) + self.b_h
            )
            H[:, t, :] = h_t
            h_prev = h_t

        return H


if __name__ == "__main__":
    print("--- Running Elman RNN Forward Pass Verification ---")
    np.random.seed(42)

    # Sequence parameters: 3 features, length 4, batch size 2
    d, T, N = 3, 4, 2
    h = 5  # Hidden dimension

    rnn = ElmanRNNNumPy(in_features=d, hidden_dim=h)
    X = np.random.randn(d, T, N)

    # Compute forward pass
    H = rnn.forward(X)
    print("Hidden states tensor shape:", H.shape)
    assert H.shape == (h, T, N)

    # Verify transition logic for step 0 manually:
    # h_0 = tanh(W_hh * zero + W_xh * x_0 + b_h)
    x_0 = X[:, 0, :]
    expected_h_0 = np.tanh(np.dot(rnn.W_xh, x_0) + rnn.b_h)
    assert np.allclose(H[:, 0, :], expected_h_0)
    print("Step 0 hidden state transition verified.")

    # Verify transition logic for step 1:
    h_0_prev = H[:, 0, :]
    x_1 = X[:, 1, :]
    expected_h_1 = np.tanh(np.dot(rnn.W_hh, h_0_prev) + np.dot(rnn.W_xh, x_1) + rnn.b_h)
    assert np.allclose(H[:, 1, :], expected_h_1)
    print("Step 1 hidden state transition verified.")

    print("\n  [PASS] RNN forward pass shapes and outputs verified.")
