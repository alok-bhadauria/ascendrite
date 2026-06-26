import numpy as np


def compute_empirical_rademacher_complexity(
    X: np.ndarray,
    hypotheses: np.ndarray,
    n_trials: int = 1000
) -> float:
    """Computes the empirical Rademacher complexity of a linear classifier hypothesis class

    on a given input feature matrix X.

    Definition:
        R_s(H) = E_sigma [ sup_{h in H} (1/N) * sum_{i=1}^N sigma_i * h(x_i) ]
        where sigma_i are independent Rademacher random variables taking values in {-1, 1}.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        hypotheses: Matrix of shape (n_hypotheses, n_features) representing the weight
                    vectors of linear classifiers.
        n_trials: Number of Monte Carlo simulation trials to approximate the expectation.

    Returns:
        float: The empirical Rademacher complexity.
    """
    n_samples, n_features = X.shape
    n_hypotheses = hypotheses.shape[0]

    # Precompute model predictions for all hypotheses
    # predictions shape: (n_hypotheses, n_samples) with values in {-1, 1}
    predictions = np.sign(hypotheses @ X.T)
    # Replace any exact 0 predictions with 1 (standard sign function behavior)
    predictions[predictions == 0.0] = 1.0

    sum_max_correlations = 0.0

    for _ in range(n_trials):
        # 1. Generate independent Rademacher random variables (random labels {-1, 1})
        sigmas = np.random.choice([-1.0, 1.0], size=n_samples)

        # 2. Compute correlation for each hypothesis: (1/N) * sum_i sigma_i * h(x_i)
        # predictions shape is (n_hypotheses, n_samples), sigmas shape is (n_samples,)
        # result shape is (n_hypotheses,)
        correlations = (predictions @ sigmas) / n_samples

        # 3. Find the supremum (maximum correlation) over the hypothesis class
        supremum = np.max(correlations)

        sum_max_correlations += supremum

    # Return the expected value over the trials
    return float(sum_max_correlations / n_trials)
