import numpy as np


def calculate_gini_impurity(y: np.ndarray) -> float:
    """Computes the Gini Impurity of a label array y.

    Formula:
        Gini = 1 - sum(p_k^2)
    """
    n_samples = len(y)
    if n_samples == 0:
        return 0.0

    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / n_samples
    gini = 1.0 - np.sum(probabilities ** 2)
    return float(gini)


def find_best_split(X: np.ndarray, y: np.ndarray) -> dict:
    """Scans all features and candidate thresholds to find the split that maximizes Information Gain.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        y: Labels vector of shape (n_samples,).

    Returns:
        dict: Details of the best split:
            - "feature_idx": Index of the optimal feature.
            - "threshold": Value of the optimal threshold.
            - "info_gain": Maximum Information Gain achieved.
    """
    n_samples, n_features = X.shape
    parent_impurity = calculate_gini_impurity(y)

    best_split = {
        "feature_idx": None,
        "threshold": None,
        "info_gain": -1.0,
    }

    for feature_idx in range(n_features):
        # Extract feature values and sort them
        feature_values = X[:, feature_idx]
        sorted_indices = np.argsort(feature_values)
        X_sorted = feature_values[sorted_indices]
        y_sorted = y[sorted_indices]

        # Scan candidate thresholds (midpoints between consecutive unique values)
        for i in range(1, n_samples):
            # Skip if adjacent values are identical (no boundary exists)
            if X_sorted[i] == X_sorted[i - 1]:
                continue

            threshold = (X_sorted[i] + X_sorted[i - 1]) / 2.0

            # Partition labels
            y_left = y_sorted[:i]
            y_right = y_sorted[i:]

            # Compute child impurities
            impurity_left = calculate_gini_impurity(y_left)
            impurity_right = calculate_gini_impurity(y_right)

            # Weighted child impurity
            n_left = len(y_left)
            n_right = len(y_right)
            child_impurity = (n_left / n_samples) * impurity_left + (n_right / n_samples) * impurity_right

            # Information Gain
            info_gain = parent_impurity - child_impurity

            if info_gain > best_split["info_gain"]:
                best_split["feature_idx"] = feature_idx
                best_split["threshold"] = threshold
                best_split["info_gain"] = float(info_gain)

    return best_split


if __name__ == "__main__":
    # Generate simple non-linear synthetic dataset
    np.random.seed(42)
    X_data = np.random.uniform(-1, 1, (100, 2))
    # Class 1 if inside a quadrant, Class 0 otherwise
    y_data = np.where((X_data[:, 0] > 0) & (X_data[:, 1] > 0), 1, 0)

    # Find the best root split
    split_info = find_best_split(X_data, y_data)

    print("Decision Tree Splitting Search (Pure NumPy):")
    print(f"Parent Gini Impurity: {calculate_gini_impurity(y_data):.5f}")
    print(f"Best Split Feature Index: {split_info['feature_idx']}")
    print(f"Best Split Threshold:     {split_info['threshold']:.5f}")
    print(f"Max Information Gain:     {split_info['info_gain']:.5f}")
