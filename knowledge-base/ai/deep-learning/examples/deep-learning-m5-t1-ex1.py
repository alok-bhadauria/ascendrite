import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


class UndercompleteAutoencoderNumPy:
    """Implements an undercomplete Autoencoder forward pass in NumPy."""

    def __init__(self, input_dim: int, latent_dim: int):
        self.D = input_dim
        self.d = latent_dim
        assert self.d < self.D, "Latent dimension must be smaller than input dimension (undercomplete)!"

        # Initialize weights
        self.W_e = np.random.randn(self.d, self.D) * 0.1
        self.b_e = np.zeros((self.d, 1))

        self.W_d = np.random.randn(self.D, self.d) * 0.1
        self.b_d = np.zeros((self.D, 1))

    def encode(self, X: np.ndarray) -> np.ndarray:
        """Projects input to latent space."""
        return sigmoid(np.dot(self.W_e, X) + self.b_e)

    def decode(self, Z: np.ndarray) -> np.ndarray:
        """Reconstructs input from latent representation."""
        return sigmoid(np.dot(self.W_d, Z) + self.b_d)

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Runs the full autoencoder mapping."""
        Z = self.encode(X)
        X_hat = self.decode(Z)
        return X_hat, Z

    def compute_mse_loss(self, X: np.ndarray, X_hat: np.ndarray) -> float:
        """Computes Mean Squared Error reconstruction loss.

        Loss = 1/(2*N) * sum_i ||x_i - x_hat_i||^2
        """
        N = X.shape[1]
        loss = 0.5 * np.sum((X - X_hat) ** 2) / N
        return loss


if __name__ == "__main__":
    print("--- Running Undercomplete Autoencoder Verification ---")
    np.random.seed(42)

    # Input dimension D=5, bottleneck d=2, batch size N=3
    D, d, N = 5, 2, 3
    ae = UndercompleteAutoencoderNumPy(input_dim=D, latent_dim=d)

    X = np.random.rand(D, N)  # Normalized inputs bounded in [0, 1]

    # Forward mapping
    X_hat, Z = ae.forward(X)
    print("Latent space representation shape:", Z.shape)
    print("Reconstructed output shape:", X_hat.shape)

    assert Z.shape == (d, N)
    assert X_hat.shape == (D, N)

    # Verify reconstruction loss output
    loss = ae.compute_mse_loss(X, X_hat)
    print(f"Reconstruction MSE loss: {loss:.5f}")
    
    # Check manual loss calculation
    expected_loss = 0.5 * np.sum((X - X_hat) ** 2) / N
    assert np.isclose(loss, expected_loss)
    print("Reconstruction loss computation verified.")

    print("\n  [PASS] Autoencoder example verified successfully.")
