import numpy as np


def step_decay(epoch: int, eta_0: float, gamma: float, step_size: int) -> float:
    """Decays the learning rate by gamma every step_size epochs.

    eta_t = eta_0 * gamma^(floor(epoch / step_size))
    """
    exponent = int(np.floor(epoch / step_size))
    return eta_0 * (gamma**exponent)


def cosine_annealing(
    epoch: int, T_max: int, eta_max: float, eta_min: float = 0.0
) -> float:
    """Applies Cosine Annealing to adjust the learning rate dynamically.

    eta_t = eta_min + 0.5 * (eta_max - eta_min) * (1 + cos(epoch / T_max * pi))
    """
    # Clamp epoch to T_max to prevent out-of-bounds scheduling
    t = min(epoch, T_max)
    cos_val = np.cos((t / T_max) * np.pi)
    return eta_min + 0.5 * (eta_max - eta_min) * (1.0 + cos_val)


if __name__ == "__main__":
    print("--- Running Learning Rate Scheduler Practice ---")

    # 1. Test Step Decay
    eta_0 = 0.1
    gamma = 0.5
    step_size = 10

    # At epoch 0, 5, 10, 20
    assert np.isclose(step_decay(0, eta_0, gamma, step_size), 0.1)
    assert np.isclose(step_decay(5, eta_0, gamma, step_size), 0.1)
    assert np.isclose(step_decay(10, eta_0, gamma, step_size), 0.05)
    assert np.isclose(step_decay(20, eta_0, gamma, step_size), 0.025)
    print("  [PASS] Step decay scheduler verified.")

    # 2. Test Cosine Annealing
    eta_max = 0.01
    eta_min = 0.001
    T_max = 50

    # At epoch 0: should be eta_max
    assert np.isclose(cosine_annealing(0, T_max, eta_max, eta_min), 0.01)
    # At epoch T_max / 2 (25): should be intermediate value: eta_min + 0.5*(eta_max-eta_min) = 0.0055
    assert np.isclose(cosine_annealing(25, T_max, eta_max, eta_min), 0.0055)
    # At epoch T_max (50): should be eta_min
    assert np.isclose(cosine_annealing(50, T_max, eta_max, eta_min), 0.001)
    print("  [PASS] Cosine annealing scheduler verified.")

    print("\nAll scheduler checks completed successfully!")
