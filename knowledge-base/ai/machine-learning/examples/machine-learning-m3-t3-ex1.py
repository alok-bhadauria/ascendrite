import numpy as np


class MultinomialNaiveBayes:
    """Multinomial Naive Bayes classifier with Laplace smoothing."""

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.classes = None
        self.class_log_prior = None
        self.feature_log_prob = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "MultinomialNaiveBayes":
        """Fits the classifier by calculating log priors and Laplace-smoothed log likelihoods."""
        n_samples, n_features = X.shape
        self.classes = np.unique(y)
        n_classes = len(self.classes)

        self.class_log_prior = np.zeros(n_classes)
        self.feature_log_prob = np.zeros((n_classes, n_features))

        for c_idx, c in enumerate(self.classes):
            X_c = X[y == c]
            # Prior: P(Y = c)
            self.class_log_prior[c_idx] = np.log(X_c.shape[0] / n_samples)

            # Sum of feature counts for class c: N_c_j for each feature j
            feature_counts = X_c.sum(axis=0)

            # Total count of features in class c: N_c
            total_count = feature_counts.sum()

            # Laplace-smoothed log likelihoods: log((N_c_j + alpha) / (N_c + alpha * V))
            smoothed_likelihoods = (feature_counts + self.alpha) / (
                total_count + self.alpha * n_features
            )
            self.feature_log_prob[c_idx, :] = np.log(smoothed_likelihoods)

        return self

    def predict_log_proba(self, X: np.ndarray) -> np.ndarray:
        """Calculates joint log probabilities: log P(Y) + sum(log P(X_i | Y))."""
        # X: (n_queries, n_features), feature_log_prob.T: (n_features, n_classes)
        # Result: (n_queries, n_classes)
        return X @ self.feature_log_prob.T + self.class_log_prior

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicts class labels for the query matrix X."""
        log_prob = self.predict_log_proba(X)
        return self.classes[np.argmax(log_prob, axis=1)]


def calculate_minkowski_distance(
    x1: np.ndarray, x2: np.ndarray, p: float
) -> float:
    """Computes the Minkowski distance between two vectors for a given p order."""
    return float(np.sum(np.abs(x1 - x2) ** p) ** (1.0 / p))
