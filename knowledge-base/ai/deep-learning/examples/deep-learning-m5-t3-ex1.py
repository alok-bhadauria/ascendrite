import numpy as np


def compute_gan_losses(
    D_real: np.ndarray, D_fake: np.ndarray
) -> tuple[float, float, float]:
    """Computes the standard minimax and non-saturating losses for GANs.

    Args:
        D_real: Discriminator outputs for real samples, shape (N, 1) or (N,)
        D_fake: Discriminator outputs for generated samples, shape (N, 1) or (N,)

    Returns:
        tuple containing:
            - loss_D: Discriminator loss (minimizing this maximizes the value function)
            - loss_G_minimax: Standard minimax Generator loss
            - loss_G_heuristic: Non-saturating heuristic Generator loss
    """
    N = len(D_real)
    eps = 1e-12  # Epsilon to avoid log(0)

    # 1. Discriminator Loss
    # L_D = -1/N * sum( log(D(x)) + log(1 - D(G(z))) )
    loss_D = -np.mean(np.log(D_real + eps) + np.log(1.0 - D_fake + eps))

    # 2. Standard Minimax Generator Loss
    # L_G = 1/N * sum( log(1 - D(G(z))) )
    loss_G_minimax = np.mean(np.log(1.0 - D_fake + eps))

    # 3. Non-Saturating Heuristic Generator Loss
    # L_G_heuristic = -1/N * sum( log(D(G(z))) )
    loss_G_heuristic = -np.mean(np.log(D_fake + eps))

    return float(loss_D), float(loss_G_minimax), float(loss_G_heuristic)


if __name__ == "__main__":
    print("--- Running GAN Value Loss Verification ---")

    # Mock predictions for batch of size N=3
    # Case 1: Early training - Discriminator is highly confident, Generator is poor
    # D_real outputs are close to 1.0 (correctly identified as real)
    # D_fake outputs are close to 0.0 (correctly identified as fake)
    D_real_1 = np.array([[0.99], [0.95], [0.98]])
    D_fake_1 = np.array([[0.01], [0.05], [0.02]])

    loss_D_1, loss_G_mini_1, loss_G_heur_1 = compute_gan_losses(D_real_1, D_fake_1)
    print(f"Case 1 (Early) - D Loss: {loss_D_1:.5f}, G Minimax: {loss_G_mini_1:.5f}, G Heuristic: {loss_G_heur_1:.5f}")

    # Assertions for Case 1
    # D loss should be small because it classifies correctly
    assert loss_D_1 < 0.1
    # G minimax loss should be very small (close to 0), yielding vanishing gradients
    assert abs(loss_G_mini_1) < 0.05
    # G heuristic loss should be large, providing strong gradient signals
    assert loss_G_heur_1 > 2.5
    print("Heuristic gradient strength vs minimax vanishing gradient confirmed.")

    # Case 2: Nash equilibrium (p_g = p_data)
    # Discriminator outputs exactly 0.5 everywhere (complete uncertainty)
    D_real_2 = np.ones((3, 1)) * 0.5
    D_fake_2 = np.ones((3, 1)) * 0.5
    loss_D_2, loss_G_mini_2, loss_G_heur_2 = compute_gan_losses(D_real_2, D_fake_2)
    print(f"Case 2 (Nash) - D Loss: {loss_D_2:.5f}, G Minimax: {loss_G_mini_2:.5f}")

    # Expected value for log(0.5) is -0.693147
    # L_D = - (log(0.5) + log(0.5)) = -2 * log(0.5) = 2 * 0.693147 = 1.38629
    assert np.isclose(loss_D_2, -2.0 * np.log(0.5))
    assert np.isclose(loss_G_mini_2, np.log(0.5))
    print("Nash equilibrium values verified.")

    print("\n  [PASS] GAN loss examples verified successfully.")
