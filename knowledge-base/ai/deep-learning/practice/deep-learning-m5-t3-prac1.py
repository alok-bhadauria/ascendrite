import numpy as np


def compute_discriminator_bce(D_real: np.ndarray, D_fake: np.ndarray) -> float:
    """Calculates the binary cross-entropy loss for the discriminator.

    L = - (1 / N) * sum_i ( log(D_real_i) + log(1 - D_fake_i) )
    """
    N = len(D_real)
    # Binary cross entropy terms for real (target=1) and fake (target=0)
    loss = -np.mean(np.log(D_real) + np.log(1.0 - D_fake))
    return float(loss)


if __name__ == "__main__":
    print("--- Running GAN Loss Calculation Practice ---")

    D_real = np.array([0.8, 0.9])
    D_fake = np.array([0.2, 0.1])

    # Log calculations:
    # log(D_real) = [log(0.8), log(0.9)] = [-0.22314355, -0.10536052]
    # log(1 - D_fake) = [log(0.8), log(0.9)] = [-0.22314355, -0.10536052]
    # Sum of terms = 2 * (-0.22314355 - 0.10536052) = -0.65700814
    # Mean (divided by N=2) = -0.32850407
    # Loss = -(-0.32850407) = 0.32850407
    loss = compute_discriminator_bce(D_real, D_fake)
    print("Calculated discriminator loss:", loss)

    expected = -np.mean(np.log(D_real) + np.log(1.0 - D_fake))
    assert np.isclose(loss, expected)
    print("Discriminator loss matches expected manual calculation.")

    print("\n  [PASS] Discriminator loss practice verified successfully.")
