import numpy as np


def compute_reconstruction_mse(X: np.ndarray, X_hat: np.ndarray) -> float:
    """Computes the reconstruction Mean Squared Error (MSE) loss.

    The loss is defined as:
    L = (1 / (2 * N)) * sum_{i=1}^N ||x_i - x_hat_i||_2^2
    where N is the number of samples (columns of X).
    """
    N = X.shape[1]
    # Sum of squared differences scaled by 1/(2*N)
    loss = 0.5 * np.sum((X - X_hat) ** 2) / N
    return loss


if __name__ == "__main__":
    print("--- Running Reconstruction MSE Loss Practice ---")

    # Inputs with dimensions (D=3, N=2)
    X = np.array(
        [[1.0, 2.0],
         [0.0, 1.0],
         [-1.0, 0.5]]
    )

    X_hat = np.array(
        [[0.8, 1.8],
         [0.2, 0.9],
         [-0.9, 0.7]]
    )

    # Squared differences:
    # Sample 0: (1-0.8)^2 + (0-0.2)^2 + (-1 - -0.9)^2 = 0.04 + 0.04 + 0.01 = 0.09
    # Sample 1: (2-1.8)^2 + (1-0.9)^2 + (0.5 - 0.7)^2 = 0.04 + 0.01 + 0.04 = 0.09
    # Total sum = 0.09 + 0.09 = 0.18
    # Loss = 0.5 * 0.18 / 2 = 0.045
    loss = compute_reconstruction_mse(X, X_hat)
    print("Calculated loss:", loss)
    assert np.isclose(loss, 0.045)
    print("Reconstruction loss matches expected manual calculation.")

    print("\n  [PASS] Reconstruction loss practice verified successfully.")
