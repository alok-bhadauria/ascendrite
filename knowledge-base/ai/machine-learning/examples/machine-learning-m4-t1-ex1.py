import numpy as np


def generate_noisy_data(n_samples: int, noise_std: float = 0.3) -> tuple[np.ndarray, np.ndarray]:
    """Generates synthetic samples from y = sin(pi * x) + noise."""
    x = np.random.uniform(-1.0, 1.0, n_samples)
    y = np.sin(np.pi * x) + np.random.normal(0, noise_std, n_samples)
    return x, y


def fit_polynomial(x: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    """Fits a polynomial of a given degree to (x, y) and returns coefficients."""
    return np.polyfit(x, y, degree)


def evaluate_polynomial(coefficients: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Evaluates the polynomial at given points x."""
    return np.polyval(coefficients, x)


def run_bias_variance_simulation(
    n_datasets: int = 100,
    n_samples: int = 20,
    degrees: list[int] = None,
    noise_std: float = 0.3
) -> dict[int, dict[str, float]]:
    """Runs a Monte Carlo simulation to decompose expected error into Bias^2 and Variance.

    Iteratively generates n_datasets, fits polynomials of varying degrees,
    and computes the squared bias and variance over a fixed test grid.
    """
    if degrees is None:
        degrees = [1, 3, 10]

    # Fixed evaluation grid
    x_test = np.linspace(-1.0, 1.0, 100)
    y_test_true = np.sin(np.pi * x_test)

    results = {}

    for deg in degrees:
        all_predictions = np.zeros((n_datasets, len(x_test)))

        for d_idx in range(n_datasets):
            # 1. Draw a random training dataset
            x_train, y_train = generate_noisy_data(n_samples, noise_std)

            # 2. Fit model
            coeffs = fit_polynomial(x_train, y_train, deg)

            # 3. Predict on test grid
            all_predictions[d_idx] = evaluate_polynomial(coeffs, x_test)

        # Compute expectations over the datasets
        # E[f_hat(x)]
        mean_prediction = np.mean(all_predictions, axis=0)

        # Squared Bias: (E[f_hat(x)] - f(x))^2
        squared_bias = np.mean((mean_prediction - y_test_true) ** 2)

        # Variance: E[(f_hat(x) - E[f_hat(x)])^2]
        variance = np.mean(np.var(all_predictions, axis=0))

        # Irreducible error is noise_std^2
        irreducible_error = noise_std ** 2

        # Expected Prediction Error: E[(y - f_hat(x))^2]
        # We compute this directly from predictions to verify additive decomposition
        expected_error = np.mean((all_predictions - y_test_true[np.newaxis, :]) ** 2) + irreducible_error

        results[deg] = {
            "squared_bias": float(squared_bias),
            "variance": float(variance),
            "irreducible_error": float(irreducible_error),
            "expected_error": float(expected_error),
        }

    return results


if __name__ == "__main__":
    # Run simulation and print results
    sim_results = run_bias_variance_simulation(n_datasets=200, n_samples=30, degrees=[1, 3, 10])
    for degree, metrics in sim_results.items():
        print(f"Polynomial Degree {degree:2d}:")
        print(f"  Bias^2:            {metrics['squared_bias']:.5f}")
        print(f"  Variance:          {metrics['variance']:.5f}")
        print(f"  Irreducible Error: {metrics['irreducible_error']:.5f}")
        print(f"  Expected Error:    {metrics['expected_error']:.5f}")
        summed = metrics['squared_bias'] + metrics['variance'] + metrics['irreducible_error']
        print(f"  Bias^2+Var+Noise:  {summed:.5f}\n")
