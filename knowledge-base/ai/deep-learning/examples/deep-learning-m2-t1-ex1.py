import numpy as np


def loss_and_grad(theta: np.ndarray) -> tuple[float, np.ndarray]:
    """Computes the loss and gradient for an anisotropic quadratic valley.

    f(x, y) = 0.5 * x^2 + 10 * y^2
    This surface has high curvature along y and low curvature along x.
    """
    x, y = theta[0, 0], theta[1, 0]
    loss = 0.5 * (x**2) + 10.0 * (y**2)
    grad = np.array([[x], [20.0 * y]])
    return loss, grad


def run_sgd(
    init_theta: np.ndarray, lr: float, steps: int
) -> list[tuple[float, float]]:
    theta = init_theta.copy()
    history = []
    for _ in range(steps):
        loss, grad = loss_and_grad(theta)
        history.append((theta[0, 0], theta[1, 0]))
        theta = theta - lr * grad
    return history


def run_momentum(
    init_theta: np.ndarray, lr: float, beta: float, steps: int
) -> list[tuple[float, float]]:
    theta = init_theta.copy()
    v = np.zeros_like(theta)
    history = []
    for _ in range(steps):
        loss, grad = loss_and_grad(theta)
        history.append((theta[0, 0], theta[1, 0]))
        v = beta * v + lr * grad
        theta = theta - v
    return history


def run_nesterov(
    init_theta: np.ndarray, lr: float, beta: float, steps: int
) -> list[tuple[float, float]]:
    theta = init_theta.copy()
    v = np.zeros_like(theta)
    history = []
    for _ in range(steps):
        # Nesterov gradient evaluation at look-ahead point (theta - beta * v)
        look_ahead = theta - beta * v
        loss, grad = loss_and_grad(look_ahead)
        history.append((theta[0, 0], theta[1, 0]))
        v = beta * v + lr * grad
        theta = theta - v
    return history


if __name__ == "__main__":
    print("--- Optimizer Comparison on Anisotropic Valley ---")

    # Start at a point far from the optimum (0, 0)
    init_pos = np.array([[10.0], [1.0]])
    steps = 30
    lr = 0.04  # Stable learning rate under anisotropic curvature
    beta = 0.6

    # 1. Run standard SGD
    sgd_path = run_sgd(init_pos, lr, steps)
    print("\nSGD Path (first 5 steps):")
    for i, p in enumerate(sgd_path[:5]):
        print(f"  Step {i}: x = {p[0]:.4f}, y = {p[1]:.4f}")

    # 2. Run Momentum SGD
    momentum_path = run_momentum(init_pos, lr, beta, steps)
    print("\nClassical Momentum Path (first 5 steps):")
    for i, p in enumerate(momentum_path[:5]):
        print(f"  Step {i}: x = {p[0]:.4f}, y = {p[1]:.4f}")

    # 3. Run Nesterov Accelerated Gradient
    nesterov_path = run_nesterov(init_pos, lr, beta, steps)
    print("\nNesterov Momentum Path (first 5 steps):")
    for i, p in enumerate(nesterov_path[:5]):
        print(f"  Step {i}: x = {p[0]:.4f}, y = {p[1]:.4f}")

    # Metric comparison: check distance to minimum (0, 0) at the end of runs
    final_sgd_dist = np.linalg.norm(np.array(sgd_path[-1]))
    final_momentum_dist = np.linalg.norm(np.array(momentum_path[-1]))
    final_nesterov_dist = np.linalg.norm(np.array(nesterov_path[-1]))

    print(f"\nFinal Euclidean Distance to Optimum after {steps} steps:")
    print(f"  Standard SGD:        {final_sgd_dist:.6f}")
    print(f"  Classical Momentum:  {final_momentum_dist:.6f}")
    print(f"  Nesterov Momentum:   {final_nesterov_dist:.6f}")

    # Momentum should damp oscillations and progress much closer to 0 than standard SGD
    assert (
        final_momentum_dist < final_sgd_dist
    ), "Momentum should outperform standard SGD!"
    assert (
        final_nesterov_dist < final_sgd_dist
    ), "Nesterov should outperform standard SGD!"

    print("\n  [PASS] Momentum-based optimizers damp oscillations and accelerate convergence.")
