import numpy as np


def reparameterize_practice(
    mu: np.ndarray, std: np.ndarray, eps: np.ndarray
) -> np.ndarray:
    """Computes the latent code z using the reparameterization trick.

    z = mu + std * eps
    """
    z = mu + std * eps
    return z


if __name__ == "__main__":
    print("--- Running VAE Reparameterization Practice ---")

    mu = np.array([[0.5], [-1.0]])
    std = np.array([[0.1], [0.2]])
    eps = np.array([[1.5], [-0.5]])

    z = reparameterize_practice(mu, std, eps)
    print("Calculated latent code:\n", z)

    # z[0] = 0.5 + 0.1 * 1.5 = 0.5 + 0.15 = 0.65
    # z[1] = -1.0 + 0.2 * -0.5 = -1.0 - 0.1 = -1.1
    expected = np.array([[0.65], [-1.1]])
    assert np.allclose(z, expected)
    print("Reparameterization output matches manual calculation.")

    print("\n  [PASS] Reparameterization practice verified successfully.")
