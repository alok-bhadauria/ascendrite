import numpy as np


class DecisionStub:
    """A 1-level Decision Tree (Stub) for classification with weighted samples."""

    def __init__(self):
        self.polarity = 1
        self.feature_idx = None
        self.threshold = None
        self.alpha = None

    def predict(self, X: np.ndarray) -> np.ndarray:
        n_samples = X.shape[0]
        X_column = X[:, self.feature_idx]
        predictions = np.ones(n_samples)
        if self.polarity == 1:
            predictions[X_column < self.threshold] = -1
        else:
            predictions[X_column > self.threshold] = -1
        return predictions


class AdaBoost:
    """AdaBoost classifier with decision stubs as weak learners, implemented in pure NumPy."""

    def __init__(self, n_estimators: int = 5):
        self.n_estimators = n_estimators
        self.clfs = []

    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape

        # Initialize uniform sample weights: w_i = 1/N
        w = np.full(n_samples, 1.0 / n_samples)

        for t in range(self.n_estimators):
            clf = DecisionStub()
            min_error = float("inf")

            # Greedy search for the best split threshold and feature to minimize weighted error
            for feature_i in range(n_features):
                X_column = X[:, feature_i]
                thresholds = np.unique(X_column)

                for threshold in thresholds:
                    # Check both polarities
                    for polarity in [1, -1]:
                        predictions = np.ones(n_samples)
                        if polarity == 1:
                            predictions[X_column < threshold] = -1
                        else:
                            predictions[X_column > threshold] = -1

                        # Calculate weighted error: sum(w_i * I(y_i != h(x_i)))
                        misclassified = y != predictions
                        error = np.dot(w, misclassified)

                        if error < min_error:
                            min_error = error
                            clf.polarity = polarity
                            clf.feature_idx = feature_i
                            clf.threshold = threshold

            # Avoid division by zero if error is 0
            err_eps = 1e-15
            error_rate = max(min_error, err_eps)

            # Compute classifier weight beta (alpha in standard textbooks)
            # beta = 0.5 * log((1 - err) / err)
            clf.alpha = 0.5 * np.log((1.0 - error_rate) / error_rate)

            # Get predictions of the chosen stub
            predictions = clf.predict(X)

            # Update sample weights: w = w * exp(-alpha * y * h(x))
            w = w * np.exp(-clf.alpha * y * predictions)
            # Re-normalize weights to sum to 1.0
            w = w / np.sum(w)

            self.clfs.append(clf)

            print(f"Iteration {t:2d} | Feature Split: {clf.feature_idx} | Threshold: {clf.threshold:6.2f} | Weighted Error: {error_rate:.5f} | Step Size: {clf.alpha:.5f}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Computes predictions using sign(sum(alpha_m * h_m(x)))."""
        clf_preds = [clf.alpha * clf.predict(X) for clf in self.clfs]
        y_pred = np.sum(clf_preds, axis=0)
        return np.sign(y_pred)


if __name__ == "__main__":
    # Generate linear non-separable synthetic classification dataset
    np.random.seed(42)
    X_data = np.random.randn(100, 2)
    # Target label y in {-1, 1}
    y_data = np.where(X_data[:, 0] + X_data[:, 1] > 0.5, 1, -1)

    print("Fitting AdaBoost Classifier (Pure NumPy):")
    model = AdaBoost(n_estimators=5)
    model.fit(X_data, y_data)

    train_preds = model.predict(X_data)
    train_acc = np.mean(train_preds == y_data)
    print(f"\nFinal AdaBoost Train Accuracy: {train_acc * 100:.2f}%")
