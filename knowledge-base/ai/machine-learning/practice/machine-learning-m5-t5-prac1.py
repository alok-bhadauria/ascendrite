import numpy as np


def calculate_psi(
    baseline: np.ndarray,
    target: np.ndarray,
    num_bins: int = 10,
    epsilon: float = 1e-4,
) -> float:
    """Computes the Population Stability Index (PSI) between baseline and target distributions.

    Args:
        baseline: 1D NumPy array of reference/training feature values.
        target: 1D NumPy array of production/new feature values.
        num_bins: Number of bins to use (default 10 for deciles).
        epsilon: Small constant added to bin proportions to avoid division by zero
          or log of zero.

    Returns:
        float: Computed PSI value.
    """
    # 1. Establish bin boundaries based on baseline quantiles
    percentiles = np.linspace(0, 100, num_bins + 1)
    bin_edges = np.percentile(baseline, percentiles)

    # Adjust bin edges to handle duplicate values and ensure bounds cover all data
    bin_edges[0] -= 1e-9
    bin_edges[-1] += 1e-9

    # 2. Count samples in each bin
    baseline_counts, _ = np.histogram(baseline, bins=bin_edges)
    target_counts, _ = np.histogram(target, bins=bin_edges)

    # 3. Convert counts to proportions
    n_base = len(baseline)
    n_target = len(target)

    actual_props = baseline_counts / n_base
    expected_props = target_counts / n_target

    # 4. Apply Laplace-style smoothing to avoid division by zero or log of zero
    actual_props = np.where(actual_props == 0, epsilon, actual_props)
    expected_props = np.where(expected_props == 0, epsilon, expected_props)

    # Normalize again to ensure sum is exactly 1.0 (though minor)
    actual_props /= np.sum(actual_props)
    expected_props /= np.sum(expected_props)

    # 5. Compute PSI = sum((expected - actual) * ln(expected / actual))
    psi_value = np.sum((expected_props - actual_props) * np.log(expected_props / actual_props))

    return float(psi_value)


def kolmogorov_smirnov_two_sample(
    baseline: np.ndarray, target: np.ndarray, alpha: float = 0.05
) -> tuple[float, bool]:
    """Computes the two-sample Kolmogorov-Smirnov test statistic.

    Determines whether the target distribution significantly drifts from the baseline.

    Args:
        baseline: 1D NumPy array representing baseline data.
        target: 1D NumPy array representing target (production) data.
        alpha: Significance level for the hypothesis test (typically 0.05).

    Returns:
        tuple[float, bool]:
            - ks_statistic: The supremum of absolute differences between the two ECDFs.
            - drift_detected: True if we reject the null hypothesis of identical distributions.
    """
    n = len(baseline)
    m = len(target)

    # Sort baseline and target to allow proper searchsorted ECDF calculations
    sorted_baseline = np.sort(baseline)
    sorted_target = np.sort(target)

    # Combine and sort all unique observations to evaluate ECDFs
    combined = np.sort(np.concatenate([sorted_baseline, sorted_target]))

    # Compute ECDF for baseline
    # ECDF_1(x) = (count of baseline samples <= x) / n
    # np.searchsorted(..., side='right') returns the index of the first element greater than x
    # on a sorted array, which is mathematically equivalent to the count of elements <= x.
    ecdf_baseline = np.searchsorted(sorted_baseline, combined, side="right") / n

    # Compute ECDF for target
    ecdf_target = np.searchsorted(sorted_target, combined, side="right") / m

    # KS statistic is supremum of absolute differences
    ks_statistic = float(np.max(np.abs(ecdf_baseline - ecdf_target)))

    # Calculate critical value
    # For alpha = 0.05, c(alpha) = 1.358 ~ 1.36.
    # Let's map typical alpha levels to standard constants:
    alpha_mapping = {
        0.10: 1.22,
        0.05: 1.36,
        0.01: 1.63,
        0.001: 1.95,
    }
    c_alpha = alpha_mapping.get(alpha, 1.36)

    critical_value = c_alpha * np.sqrt((n + m) / (n * m))
    drift_detected = ks_statistic > critical_value

    return ks_statistic, drift_detected
