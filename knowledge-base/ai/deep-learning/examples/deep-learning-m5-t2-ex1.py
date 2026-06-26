import numpy as np


def reparameterize(
    mu: np.ndarray, log_var: np.ndarray, eps: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """Applies the Reparameterization Trick to sample latent code z.

    z = mu + std * eps
    where eps ~ N(0, I)

    Args:
        mu: Mean vector of shape (d, N)
        log_var: Log-variance vector of shape (d, N)
        eps: Optional pre-sampled noise of shape (d, N) for testing determinism

    Returns:
        tuple containing:
            - z: Sampled latent representation of shape (d, N)
            - std: Calculated standard deviation of shape (d, N)
    """
    d, N = mu.shape
    if eps is None:
        eps = np.random.randn(d, N)

    # Compute standard deviation: std = exp(0.5 * log_var)
    std = np.exp(0.5 * log_var)

    # Compute latent representation
    z = mu + std * eps
    return z, std


def compute_kl_divergence(mu: np.ndarray, log_var: np.ndarray) -> float:
    """Computes the closed-form KL Divergence loss for Gaussian distributions.

    Loss = -0.5 * sum_j (1 + log(sigma_j^2) - mu_j^2 - sigma_j^2) / N
    """
    d, N = mu.shape
    # Element-wise KL computation
    kl_element = 1.0 + log_var - mu ** 2 - np.exp(log_var)
    # Sum over dimensions, average over batch
    kl_loss = -0.5 * np.sum(kl_element) / N
    return kl_loss


if __name__ == "__main__":
    print("--- Running VAE Reparameterization Verification ---")
    np.random.seed(42)

    # Latent dimension d=3, batch size N=2
    d, N = 3, 2
    mu = np.array([[0.0, 1.0], [0.0, -1.0], [0.5, 0.0]])
    log_var = np.array([[0.0, 0.0], [0.0, -2.0], [0.5, 0.5]])

    # 1. Test Reparameterization
    eps = np.ones((d, N)) * 0.5  # Constant noise for testing determinism
    z, std = reparameterize(mu, log_var, eps)

    print("Calculated z:\n", z)
    print("Calculated std:\n", std)

    # Expected standard deviations: e^(0.5 * log_var)
    # log_var[1, 1] = -2.0 -> std = e^(-1) = 0.36787944
    # z[1, 1] = mu[1, 1] + std * eps = -1.0 + 0.36787944 * 0.5 = -0.81606
    assert np.isclose(std[1, 1], np.exp(-1.0))
    assert np.isclose(z[1, 1], -1.0 + 0.5 * np.exp(-1.0))
    print("Reparameterization calculations verified.")

    # 2. Test KL Divergence computation
    kl_val = compute_kl_divergence(mu, log_var)
    print(f"Calculated KL Divergence: {kl_val:.5f}")

    # Manual Calculation of terms: 1 + log_var - mu^2 - exp(log_var)
    # Sample 0:
    # Dim 0: 1 + 0.0 - 0.0 - 1.0 = 0.0
    # Dim 1: 1 + 0.0 - 0.0 - 1.0 = 0.0
    # Dim 2: 1 + 0.5 - 0.25 - e^0.5 = 1.5 - 0.25 - 1.64872127 = -0.39872127
    # Sum Sample 0 = -0.39872127
    #
    # Sample 1:
    # Dim 0: 1 + 0.0 - 1.0 - 1.0 = -1.0
    # Dim 1: 1 - 2.0 - 1.0 - e^-2 = -2.0 - 0.13533528 = -2.13533528
    # Dim 2: 1 + 0.5 - 0.0 - e^0.5 = 1.5 - 1.64872127 = -0.14872127
    # Sum Sample 1 = -3.28405655
    #
    # Total sum = -0.39872127 - 3.28405655 = -3.68277782
    # KL = -0.5 * (-3.68277782) / 2 = 3.68277782 / 4 = 0.92069
    assert np.isclose(kl_val, 0.920694456)
    print("KL Divergence calculation matches manual verification.")

    print("\n  [PASS] VAE reparameterization examples verified.")
