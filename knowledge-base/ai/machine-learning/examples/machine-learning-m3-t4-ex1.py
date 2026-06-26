import numpy as np
from scipy.optimize import minimize


class DualSVM:
    """Dual formulation of Soft-Margin Support Vector Machine (SVM) supporting Linear and RBF kernels."""

    def __init__(self, C: float = 1.0, kernel: str = "linear", gamma: float = 1.0):
        self.C = C
        self.kernel_type = kernel
        self.gamma = gamma
        self.lambdas = None
        self.support_vectors = None
        self.support_labels = None
        self.bias = 0.0

    def _kernel(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        """Computes the kernel Gram matrix between X1 and X2."""
        if self.kernel_type == "linear":
            return X1 @ X2.T
        elif self.kernel_type == "rbf":
            # Compute pairwise squared distances: ||x1 - x2||^2
            sq_dists = (
                np.sum(X1**2, axis=1, keepdims=True)
                + np.sum(X2**2, axis=1)
                - 2 * (X1 @ X2.T)
            )
            return np.exp(-self.gamma * sq_dists)
        else:
            raise ValueError(f"Unknown kernel type: {self.kernel_type}")

    def fit(self, X: np.ndarray, y: np.ndarray) -> "DualSVM":
        """Fits the SVM by solving the dual quadratic programming problem."""
        n_samples = X.shape[0]

        # Precompute the kernel Gram matrix
        K = self._kernel(X, X)

        # Define the dual objective function to minimize:
        # f(lambda) = 0.5 * lambda^T * (Y^T * K * Y) * lambda - sum(lambda)
        # where Y_ij = y_i * y_j
        y_outer = np.outer(y, y)
        P = y_outer * K

        def objective(lambdas):
            return 0.5 * np.dot(lambdas, P @ lambdas) - np.sum(lambdas)

        # Inequality constraint: 0 <= lambda_i <= C
        bounds = [(0.0, self.C) for _ in range(n_samples)]

        # Equality constraint: sum(lambda_i * y_i) = 0
        constraints = {"type": "eq", "fun": lambda lambdas: np.dot(lambdas, y)}

        # Initial guess for optimization
        initial_lambdas = np.zeros(n_samples)

        # Solve quadratic programming
        result = minimize(
            objective,
            initial_lambdas,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"ftol": 1e-8, "maxiter": 1000},
        )

        if not result.success:
            raise RuntimeError(f"Optimization failed to converge: {result.message}")

        lambdas = result.x

        # Identify support vectors (threshold lambdas > 1e-5 to prune noise)
        sv_mask = lambdas > 1e-5
        self.lambdas = lambdas[sv_mask]
        self.support_vectors = X[sv_mask]
        self.support_labels = y[sv_mask]

        # Identify margin support vectors where 0 < lambda < C to solve for bias b
        margin_sv_mask = (lambdas > 1e-5) & (lambdas < self.C - 1e-5)

        if np.any(margin_sv_mask):
            # For margin support vectors, y_k * (sum_i lambda_i * y_i * K(x_i, x_k) + b) = 1
            # b = y_k - sum_i lambda_i * y_i * K(x_i, x_k)
            margin_indices = np.where(margin_sv_mask)[0]
            biases = []
            for k in margin_indices:
                prediction_sum = np.sum(
                    self.lambdas * self.support_labels * K[sv_mask, k]
                )
                biases.append(y[k] - prediction_sum)
            self.bias = float(np.mean(biases))
        else:
            # Fallback bias calculation using all support vectors if no margin support vectors exist
            biases = []
            for k in np.where(sv_mask)[0]:
                prediction_sum = np.sum(
                    self.lambdas * self.support_labels * K[sv_mask, k]
                )
                biases.append(y[k] - prediction_sum)
            self.bias = float(np.mean(biases))

        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """Computes the decision values: sum(lambda_i * y_i * K(x_i, x) + b)."""
        K_sv = self._kernel(X, self.support_vectors)
        return K_sv @ (self.lambdas * self.support_labels) + self.bias

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicts class labels {-1, 1} for the input feature matrix X."""
        decisions = self.decision_function(X)
        return np.sign(decisions)
