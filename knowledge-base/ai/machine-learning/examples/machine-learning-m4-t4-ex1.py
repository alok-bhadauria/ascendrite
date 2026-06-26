import numpy as np


class RidgeRegressor:
    """Simple Ridge Regression helper for Bagging ensemble."""

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.weights = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        X_bias = np.hstack([np.ones((n_samples, 1)), X])
        I = np.eye(n_features + 1)
        I[0, 0] = 0.0
        self.weights = np.linalg.solve(X_bias.T @ X_bias + self.alpha * I, X_bias.T @ y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        n_samples = X.shape[0]
        X_bias = np.hstack([np.ones((n_samples, 1)), X])
        return X_bias @ self.weights


class BaggedRidgeRegressor:
    """Bagged Ridge Regression ensemble with Out-of-Bag (OOB) error tracking."""

    def __init__(self, n_estimators: int = 100, alpha: float = 1.0):
        self.n_estimators = n_estimators
        self.alpha = alpha
        self.estimators = []
        self.oob_mse = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        self.estimators = []

        # Track which samples were out-of-bag for each estimator
        # oob_predictions shape: (n_samples, n_estimators), initialized to NaN
        oob_predictions = np.full((n_samples, self.n_estimators), np.nan)

        for b in range(self.n_estimators):
            # 1. Generate bootstrap indices (with replacement)
            bootstrap_idx = np.random.choice(n_samples, size=n_samples, replace=True)

            # Identify OOB indices
            in_bag_mask = np.zeros(n_samples, dtype=bool)
            in_bag_mask[bootstrap_idx] = True
            oob_idx = np.where(~in_bag_mask)[0]

            # 2. Fit estimator on bootstrap sample
            X_b = X[bootstrap_idx]
            y_b = y[bootstrap_idx]

            model = RidgeRegressor(alpha=self.alpha)
            model.fit(X_b, y_b)
            self.estimators.append(model)

            # 3. Predict on OOB samples for this estimator
            if len(oob_idx) > 0:
                oob_preds = model.predict(X[oob_idx])
                oob_predictions[oob_idx, b] = oob_preds

        # 4. Calculate OOB Error
        # For each sample, average OOB predictions from estimators that did not train on it
        final_oob_preds = np.zeros(n_samples)
        valid_oob_count = 0
        squared_errors = []

        for i in range(n_samples):
            # Get predictions for sample i where estimator b did not train on it (not NaN)
            sample_oob_preds = oob_predictions[i, ~np.isnan(oob_predictions[i])]
            if len(sample_oob_preds) > 0:
                final_oob_preds[i] = np.mean(sample_oob_preds)
                squared_errors.append((y[i] - final_oob_preds[i]) ** 2)
                valid_oob_count += 1

        self.oob_mse = float(np.mean(squared_errors)) if len(squared_errors) > 0 else None

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Averages predictions from all estimators in the ensemble."""
        predictions = np.zeros((X.shape[0], self.n_estimators))
        for b, model in enumerate(self.estimators):
            predictions[:, b] = model.predict(X)
        return np.mean(predictions, axis=1)


if __name__ == "__main__":
    # Generate synthetic regression dataset
    np.random.seed(42)
    n_samples = 150
    n_features = 8
    X_data = np.random.randn(n_samples, n_features)
    true_w = np.array([2.0, -1.0, 0.5, 0.0, 0.0, 1.5, -2.5, 0.0])
    y_data = X_data @ true_w + np.random.normal(0, 1.0, n_samples)

    # Fit ensemble model
    bagged_model = BaggedRidgeRegressor(n_estimators=100, alpha=1.0)
    bagged_model.fit(X_data, y_data)

    print("Bagged Ridge Regressor (Pure NumPy):")
    print(f"Number of Estimators: {bagged_model.n_estimators}")
    print(f"Out-of-Bag (OOB) MSE:  {bagged_model.oob_mse:.5f}")

    # Verify single Ridge regressor vs bagged Ridge regressor on training data
    single_model = RidgeRegressor(alpha=1.0)
    single_model.fit(X_data, y_data)
    single_train_mse = np.mean((y_data - single_model.predict(X_data)) ** 2)
    bagged_train_mse = np.mean((y_data - bagged_model.predict(X_data)) ** 2)

    print(f"Single Ridge Train MSE: {single_train_mse:.5f}")
    print(f"Bagged Ridge Train MSE: {bagged_train_mse:.5f}")
