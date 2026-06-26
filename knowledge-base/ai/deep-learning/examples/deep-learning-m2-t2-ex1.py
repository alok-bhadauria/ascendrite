import numpy as np


class AdaptiveOptimizersDemo:
    """Demonstrates custom implementation of RMSprop, Adam, and AdamW from scratch

    and showcases how Adam L2 regularization differs from AdamW decoupled weight decay.
    """

    def __init__(self, d_in: int):
        self.d_in = d_in
        # Initialize weights
        np.random.seed(42)
        self.w = np.random.randn(d_in, 1) * 0.1

    def loss_and_grad(
        self, X: np.ndarray, y: np.ndarray
    ) -> tuple[float, np.ndarray]:
        """MSE Loss and gradient."""
        n_samples = X.shape[0]
        preds = X @ self.w
        loss = 0.5 * np.mean((preds - y) ** 2)
        grad = (X.T @ (preds - y)) / n_samples
        return loss, grad

    def train_adam_l2(
        self,
        X: np.ndarray,
        y: np.ndarray,
        lr: float,
        wd: float,
        steps: int,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
    ):
        """Adam optimizer with standard L2 Regularization (added to gradient)."""
        m = np.zeros_like(self.w)
        v = np.zeros_like(self.w)

        for t in range(1, steps + 1):
            loss, grad = self.loss_and_grad(X, y)

            # L2 Regularization adds penalty directly to the gradient
            grad_l2 = grad + wd * self.w

            # Update moments
            m = beta1 * m + (1.0 - beta1) * grad_l2
            v = beta2 * v + (1.0 - beta2) * (grad_l2**2)

            # Bias correction
            m_hat = m / (1.0 - beta1**t)
            v_hat = v / (1.0 - beta2**t)

            # Parameter update
            self.w -= (lr / (np.sqrt(v_hat) + eps)) * m_hat

    def train_adamw(
        self,
        X: np.ndarray,
        y: np.ndarray,
        lr: float,
        wd: float,
        steps: int,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
    ):
        """AdamW optimizer with decoupled weight decay (applied directly to weight)."""
        m = np.zeros_like(self.w)
        v = np.zeros_like(self.w)

        for t in range(1, steps + 1):
            loss, grad = self.loss_and_grad(X, y)

            # Update moments using raw gradient (no regularization added here)
            m = beta1 * m + (1.0 - beta1) * grad
            v = beta2 * v + (1.0 - beta2) * (grad**2)

            # Bias correction
            m_hat = m / (1.0 - beta1**t)
            v_hat = v / (1.0 - beta2**t)

            # Decoupled weight decay step applied directly, then adaptive step
            self.w = (
                self.w
                - lr * wd * self.w
                - (lr / (np.sqrt(v_hat) + eps)) * m_hat
            )


if __name__ == "__main__":
    print("--- Adaptive Optimizers & Weight Decay Comparison ---")

    # Generate synthetic regression data
    # 100 samples, 4 features
    # Feature 0 is highly active, Feature 3 is highly sparse
    np.random.seed(42)
    X = np.random.randn(100, 4)
    X[:, 0] *= 10.0  # Large scale input -> large gradients
    X[:, 3] *= 0.1  # Small scale input -> tiny gradients

    # Target weights
    w_true = np.array([[2.0], [1.5], [-1.0], [0.5]])
    y = X @ w_true + np.random.randn(100, 1) * 0.1

    # Hyperparameters
    lr = 0.05
    wd = 0.1
    steps = 150

    # 1. Run Adam with L2 Regularization
    demo_l2 = AdaptiveOptimizersDemo(d_in=4)
    demo_l2.train_adam_l2(X, y, lr=lr, wd=wd, steps=steps)
    w_l2 = demo_l2.w.copy()

    # 2. Run AdamW (Decoupled Weight Decay)
    demo_adamw = AdaptiveOptimizersDemo(d_in=4)
    demo_adamw.train_adamw(X, y, lr=lr, wd=wd, steps=steps)
    w_adamw = demo_adamw.w.copy()

    print("\nFinal Learned Weights:")
    print("Feature Index | Target Weight | Adam (L2 Reg) | AdamW (Decoupled)")
    print("-" * 65)
    for i in range(4):
        print(
            f"     {i}       |    {w_true[i, 0]:.2f}      |    {w_l2[i, 0]:.4f}     |     {w_adamw[i, 0]:.4f}"
        )

    # Let's inspect weights of sparse feature (index 3) vs active feature (index 0)
    # Under standard L2, the sparse parameter gradient is tiny, so its running second moment v_t is tiny.
    # Therefore, the regularized term wd * w / sqrt(v_t) becomes huge, over-decaying the parameter.
    # Under AdamW, decay is decoupled and is simply lr * wd * w, independent of gradient scale.
    # Let's check that AdamW learns a weight for the sparse feature that is closer to the true weight (0.5) than Adam L2.
    error_l2_sparse = abs(w_l2[3, 0] - w_true[3, 0])
    error_adamw_sparse = abs(w_adamw[3, 0] - w_true[3, 0])

    print(f"\nSparse Weight Error (Feature 3):")
    print(f"  Adam (L2 Reg): {error_l2_sparse:.6f}")
    print(f"  AdamW:         {error_adamw_sparse:.6f}")

    assert (
        error_adamw_sparse < error_l2_sparse
    ), "AdamW should generalize better on sparse features than standard L2!"
    print("\n  [PASS] AdamW decoupled decay prevents over-regularizing sparse parameters.")
