import numpy as np


def fit_ridge(X: np.ndarray, y: np.ndarray, alpha: float) -> np.ndarray:
    """Fits Ridge regression using the closed-form normal equation."""
    n_samples, n_features = X.shape
    # Add bias dimension
    X_bias = np.hstack([np.ones((n_samples, 1)), X])
    I = np.eye(n_features + 1)
    # Do not regularize the intercept term
    I[0, 0] = 0.0

    # Solve: (X^T * X + alpha * I) * w = X^T * y
    weights = np.linalg.solve(X_bias.T @ X_bias + alpha * I, X_bias.T @ y)
    return weights


def predict_ridge(X: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Predicts targets using fitted Ridge weights."""
    n_samples = X.shape[0]
    X_bias = np.hstack([np.ones((n_samples, 1)), X])
    return X_bias @ weights


def get_kfold_indices(n_samples: int, n_splits: int, seed: int = 42) -> list[tuple[np.ndarray, np.ndarray]]:
    """Generates K-Fold train and test index pairs using pure NumPy."""
    indices = np.arange(n_samples)
    rng = np.random.default_rng(seed)
    rng.shuffle(indices)

    fold_sizes = np.full(n_splits, n_samples // n_splits)
    fold_sizes[: n_samples % n_splits] += 1

    current = 0
    splits = []
    for fold_size in fold_sizes:
        test_indices = indices[current : current + fold_size]
        train_indices = np.concatenate([indices[:current], indices[current + fold_size :]])
        splits.append((train_indices, test_indices))
        current += fold_size

    return splits


def run_nested_cv_numpy(
    X: np.ndarray,
    y: np.ndarray,
    k_outer: int = 5,
    k_inner: int = 5,
    alphas: list[float] = None
) -> list[dict[str, float]]:
    """Executes a pure NumPy implementation of Nested Cross-Validation for Ridge regression."""
    if alphas is None:
        alphas = [0.01, 0.1, 1.0, 10.0, 100.0]

    n_samples = X.shape[0]
    outer_splits = get_kfold_indices(n_samples, k_outer, seed=42)
    outer_results = []

    for outer_fold, (train_val_idx, test_idx) in enumerate(outer_splits):
        X_train_val, X_test = X[train_val_idx], X[test_idx]
        y_train_val, y_test = y[train_val_idx], y[test_idx]

        # Inner Loop: Find optimal alpha
        inner_splits = get_kfold_indices(len(train_val_idx), k_inner, seed=100 + outer_fold)
        best_alpha = None
        best_val_mse = float("inf")

        for alpha in alphas:
            inner_mses = []
            for inner_train_idx, inner_val_idx in inner_splits:
                X_train_inner = X_train_val[inner_train_idx]
                X_val_inner = X_train_val[inner_val_idx]
                y_train_inner = y_train_val[inner_train_idx]
                y_val_inner = y_train_val[inner_val_idx]

                # Fit Ridge model
                weights = fit_ridge(X_train_inner, y_train_inner, alpha)

                # Predict on inner validation fold
                preds = predict_ridge(X_val_inner, weights)
                mse = np.mean((y_val_inner - preds) ** 2)
                inner_mses.append(mse)

            mean_inner_mse = float(np.mean(inner_mses))

            if mean_inner_mse < best_val_mse:
                best_val_mse = mean_inner_mse
                best_alpha = alpha

        # Outer evaluation: Fit model on the full outer training set using the best alpha
        final_weights = fit_ridge(X_train_val, y_train_val, best_alpha)

        # Predict on outer test fold
        test_preds = predict_ridge(X_test, final_weights)
        test_mse = float(np.mean((y_test - test_preds) ** 2))

        outer_results.append({
            "outer_fold": outer_fold,
            "best_alpha": best_alpha,
            "inner_val_mse": best_val_mse,
            "outer_test_mse": test_mse,
        })

    return outer_results


if __name__ == "__main__":
    # Generate synthetic regression dataset using pure NumPy
    np.random.seed(42)
    n_samples = 200
    n_features = 10
    X_data = np.random.randn(n_samples, n_features)
    true_w = np.array([2.5, -1.5, 0.5, 0.0, 0.0, 1.2, -2.0, 0.0, 0.5, 0.0])
    y_data = X_data @ true_w + np.random.normal(0, 1.5, n_samples)

    # Run Nested CV
    results = run_nested_cv_numpy(X_data, y_data, k_outer=5, k_inner=5)

    print("Nested Cross-Validation (Pure NumPy) Results:")
    print(f"{'Fold':<6} | {'Best Alpha':<10} | {'Inner Val MSE':<15} | {'Outer Test MSE':<15}")
    print("-" * 55)
    for r in results:
        print(f"{r['outer_fold']:<6d} | {r['best_alpha']:<10.2f} | {r['inner_val_mse']:<15.5f} | {r['outer_test_mse']:<15.5f}")

    mean_test_mse = np.mean([r["outer_test_mse"] for r in results])
    print("-" * 55)
    print(f"Mean Unbiased Outer Test MSE: {mean_test_mse:.5f}")
