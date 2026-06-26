import numpy as np


class BatchNormScratch:
    """Batch Normalization layer implemented from first principles in NumPy.

    Supports forward and backward passes for 2D inputs (batch_size, features).
    """

    def __init__(self, d_in: int, eps: float = 1e-5):
        self.d_in = d_in
        self.eps = eps

        # Learnable parameters initialized to 1s and 0s
        self.gamma = np.ones((1, d_in))
        self.beta = np.zeros((1, d_in))

        # Gradient storage
        self.dgamma = None
        self.dbeta = None

        # Cache variables for backward pass
        self.cache = {}

    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward pass.

        X shape: (B, D) where B is batch size and D is features.
        """
        B, D = X.shape

        # 1. Mini-batch mean
        mean = np.mean(X, axis=0, keepdims=True)  # Shape (1, D)

        # 2. Mini-batch variance
        var = np.mean((X - mean) ** 2, axis=0, keepdims=True)  # Shape (1, D)

        # 3. Normalize
        X_hat = (X - mean) / np.sqrt(var + self.eps)  # Shape (B, D)

        # 4. Affine scale and shift
        out = self.gamma * X_hat + self.beta  # Shape (B, D)

        # Store in cache
        self.cache = {"X": X, "mean": mean, "var": var, "X_hat": X_hat}

        return out

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        """Backward pass using the unified analytical gradient equations.

        grad_output shape: (B, D)
        """
        B, D = grad_output.shape

        # Extract cached values
        X_hat = self.cache["X_hat"]
        var = self.cache["var"]

        # Gradients with respect to parameters
        self.dgamma = np.sum(grad_output * X_hat, axis=0, keepdims=True)
        self.dbeta = np.sum(grad_output, axis=0, keepdims=True)

        # Gradient w.r.t input activations X using simplified formula:
        # dX = (gamma / (B * sqrt(var + eps))) * (B * grad_out - sum(grad_out) - X_hat * sum(grad_out * X_hat))
        numerator = self.gamma
        denominator = B * np.sqrt(var + self.eps)

        term1 = B * grad_output
        term2 = np.sum(grad_output, axis=0, keepdims=True)
        term3 = X_hat * np.sum(grad_output * X_hat, axis=0, keepdims=True)

        dX = (numerator / denominator) * (term1 - term2 - term3)

        return dX


def check_bn_gradients():
    """Performs a numerical gradient check via finite differences to verify

    the mathematical correctness of the BatchNorm backward pass.
    """
    B, D = 4, 3
    np.random.seed(42)

    # Random inputs and gradients of downstream loss J
    X = np.random.randn(B, D)
    grad_output = np.random.randn(B, D)

    bn = BatchNormScratch(d_in=D)

    # Analytical Gradients
    out = bn.forward(X)
    dX_analytical = bn.backward(grad_output)
    dgamma_analytical = bn.dgamma.copy()
    dbeta_analytical = bn.dbeta.copy()

    # Function to calculate scalar loss for gradient projection
    def compute_projected_loss():
        # Using inner product with grad_output as a proxy scalar loss: J = sum(out * grad_output)
        # So dJ/dout = grad_output, which matches our downstream gradient
        return np.sum(bn.forward(X) * grad_output)

    epsilon = 1e-6
    print("--- Starting BatchNorm Gradient Checking ---")

    # 1. Check Gradient w.r.t Input X
    dX_numerical = np.zeros_like(X)
    for r in range(B):
        for c in range(D):
            original_val = X[r, c]

            # X + eps
            X[r, c] = original_val + epsilon
            loss_plus = compute_projected_loss()

            # X - eps
            X[r, c] = original_val - epsilon
            loss_minus = compute_projected_loss()

            X[r, c] = original_val  # restore
            dX_numerical[r, c] = (loss_plus - loss_minus) / (2 * epsilon)

    rel_diff_X = np.linalg.norm(dX_analytical - dX_numerical) / (
        np.linalg.norm(dX_analytical) + np.linalg.norm(dX_numerical)
    )
    print(f"Input X relative diff: {rel_diff_X:.4e}")
    assert rel_diff_X < 1e-7, f"Input X gradient check failed! Diff: {rel_diff_X}"
    print("  [PASS] Input X gradient verified.")

    # 2. Check Gradient w.r.t Gamma
    dgamma_numerical = np.zeros_like(bn.gamma)
    for c in range(D):
        original_val = bn.gamma[0, c]

        bn.gamma[0, c] = original_val + epsilon
        loss_plus = compute_projected_loss()

        bn.gamma[0, c] = original_val - epsilon
        loss_minus = compute_projected_loss()

        bn.gamma[0, c] = original_val  # restore
        dgamma_numerical[0, c] = (loss_plus - loss_minus) / (2 * epsilon)

    rel_diff_gamma = np.linalg.norm(dgamma_analytical - dgamma_numerical) / (
        np.linalg.norm(dgamma_analytical) + np.linalg.norm(dgamma_numerical)
    )
    print(f"Gamma relative diff:   {rel_diff_gamma:.4e}")
    assert (
        rel_diff_gamma < 1e-7
    ), f"Gamma gradient check failed! Diff: {rel_diff_gamma}"
    print("  [PASS] Gamma parameter gradient verified.")

    # 3. Check Gradient w.r.t Beta
    dbeta_numerical = np.zeros_like(bn.beta)
    for c in range(D):
        original_val = bn.beta[0, c]

        bn.beta[0, c] = original_val + epsilon
        loss_plus = compute_projected_loss()

        bn.beta[0, c] = original_val - epsilon
        loss_minus = compute_projected_loss()

        bn.beta[0, c] = original_val  # restore
        dbeta_numerical[0, c] = (loss_plus - loss_minus) / (2 * epsilon)

    rel_diff_beta = np.linalg.norm(dbeta_analytical - dbeta_numerical) / (
        np.linalg.norm(dbeta_analytical) + np.linalg.norm(dbeta_numerical)
    )
    print(f"Beta relative diff:    {rel_diff_beta:.4e}")
    assert (
        rel_diff_beta < 1e-7
    ), f"Beta gradient check failed! Diff: {rel_diff_beta}"
    print("  [PASS] Beta parameter gradient verified.")

    print("\nAll BatchNorm analytical gradients verified successfully!")


if __name__ == "__main__":
    check_bn_gradients()
