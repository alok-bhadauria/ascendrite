import numpy as np


def get_xavier_std(n_in: int, n_out: int) -> float:
    """Calculates the standard deviation for Xavier (Glorot) normal initialization.

    sigma = sqrt(2 / (n_in + n_out))
    """
    return np.sqrt(2.0 / (n_in + n_out))


def get_xavier_uniform_range(n_in: int, n_out: int) -> float:
    """Calculates the boundary limit 'r' for Xavier (Glorot) uniform initialization.

    Weights are drawn from U(-r, r) where r = sqrt(6 / (n_in + n_out))
    """
    return np.sqrt(6.0 / (n_in + n_out))


def get_he_std(n_in: int) -> float:
    """Calculates the standard deviation for He (Kaiming) normal initialization.

    sigma = sqrt(2 / n_in)
    """
    return np.sqrt(2.0 / n_in)


def get_he_uniform_range(n_in: int) -> float:
    """Calculates the boundary limit 'r' for He (Kaiming) uniform initialization.

    Weights are drawn from U(-r, r) where r = sqrt(6 / n_in)
    """
    return np.sqrt(6.0 / n_in)


if __name__ == "__main__":
    print("--- Running Weight Initialization Parameter Practice ---")

    n_in = 256
    n_out = 128

    # Test Xavier normal standard deviation
    x_std = get_xavier_std(n_in, n_out)
    expected_x_std = np.sqrt(2.0 / (256 + 128))
    print(f"Xavier Normal std:      {x_std:.6f} | Expected: {expected_x_std:.6f}")
    assert np.isclose(x_std, expected_x_std)

    # Test Xavier uniform boundary limit
    x_range = get_xavier_uniform_range(n_in, n_out)
    expected_x_range = np.sqrt(6.0 / (256 + 128))
    print(
        f"Xavier Uniform range:   {x_range:.6f} | Expected: {expected_x_range:.6f}"
    )
    assert np.isclose(x_range, expected_x_range)

    # Test He normal standard deviation
    he_std = get_he_std(n_in)
    expected_he_std = np.sqrt(2.0 / 256)
    print(f"He Normal std:          {he_std:.6f} | Expected: {expected_he_std:.6f}")
    assert np.isclose(he_std, expected_he_std)

    # Test He uniform boundary limit
    he_range = get_he_uniform_range(n_in)
    expected_he_range = np.sqrt(6.0 / 256)
    print(f"He Uniform range:       {he_range:.6f} | Expected: {expected_he_range:.6f}")
    assert np.isclose(he_range, expected_he_range)

    print("\n  [PASS] Weight initialization parameters checks completed successfully.")
