import numpy as np


def compute_lime_weights(
    x: np.ndarray, Z: np.ndarray, metric: str = "euclidean", sigma: float = 1.0
) -> np.ndarray:
    """Computes LIME similarity weights for perturbations around a query instance.

    The weights are calculated using the exponential similarity kernel:
        pi_x(z) = exp(-D(x, z)^2 / sigma^2)

    Args:
        x: Query instance vector of shape (n_features,).
        Z: Matrix of perturbed samples of shape (n_perturbations, n_features).
        metric: Distance metric to use ('euclidean' or 'cosine').
        sigma: Neighborhood width parameter (kernel width). Must be positive.

    Returns:
        np.ndarray: Array of similarity weights of shape (n_perturbations,).

    Raises:
        ValueError: If sigma is less than or equal to 0, or if an invalid metric
        is specified.
    """
    if sigma <= 0.0:
        raise ValueError("Kernel width sigma must be strictly positive.")

    n_perturbations, n_features = Z.shape

    # 1. Compute distances based on the specified metric
    if metric == "euclidean":
        # Compute L2 (Euclidean) distance: sqrt(sum((x - z)^2))
        distances = np.sqrt(np.sum((Z - x) ** 2, axis=1))

    elif metric == "cosine":
        # Compute Cosine distance: 1 - (x . z) / (||x|| * ||z||)
        norm_x = np.linalg.norm(x)
        norm_Z = np.linalg.norm(Z, axis=1)

        # Avoid division by zero for zero vectors
        if norm_x == 0.0:
            distances = np.ones(n_perturbations)
        else:
            dot_products = Z @ x
            # Handle elements with zero norms in Z
            norms_product = norm_x * norm_Z
            with np.errstate(invalid="ignore", divide="ignore"):
                cosine_similarity = np.where(
                    norms_product > 0.0, dot_products / norms_product, 0.0
                )
            # Clip similarities to [-1, 1] to prevent numerical issues
            cosine_similarity = np.clip(cosine_similarity, -1.0, 1.0)
            distances = 1.0 - cosine_similarity

    else:
        raise ValueError(
            f"Unsupported metric: '{metric}'. Choose 'euclidean' or 'cosine'."
        )

    # 2. Apply the exponential similarity kernel
    # pi_x(z) = exp(-D(x, z)^2 / sigma^2)
    weights = np.exp(-(distances**2) / (sigma**2))

    return weights
