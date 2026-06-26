import numpy as np


def run_deep_network(
    layer_sizes: list[int], init_mode: str, activation: str
) -> list[float]:
    """Runs a forward pass through a deep MLP and returns the variance of

    activations at each layer.
    """
    np.random.seed(42)
    B = 100  # batch size
    X = np.random.randn(B, layer_sizes[0])

    a = X
    variances = [np.var(a)]

    for i in range(len(layer_sizes) - 1):
        n_in = layer_sizes[i]
        n_out = layer_sizes[i + 1]

        # Initialize weight matrix based on selected mode
        if init_mode == "naive_small":
            # Scale too small -> vanishing activations
            W = np.random.randn(n_out, n_in) * 0.01
        elif init_mode == "naive_large":
            # Scale too large -> exploding activations
            W = np.random.randn(n_out, n_in) * 1.0
        elif init_mode == "xavier":
            # Glorot Normal: variance = 2 / (n_in + n_out)
            std = np.sqrt(2.0 / (n_in + n_out))
            W = np.random.randn(n_out, n_in) * std
        elif init_mode == "he":
            # He Normal: variance = 2 / n_in
            std = np.sqrt(2.0 / n_in)
            W = np.random.randn(n_out, n_in) * std
        else:
            raise ValueError(f"Unknown init mode: {init_mode}")

        b = np.zeros((n_out, 1))

        # Linear projection (a shape: B x n_in -> W @ a.T + b shape: n_out x B)
        z = W @ a.T + b

        # Apply activation function
        if activation == "linear":
            a = z.T
        elif activation == "tanh":
            a = np.tanh(z).T
        elif activation == "relu":
            a = np.maximum(0.0, z).T
        else:
            raise ValueError(f"Unknown activation: {activation}")

        variances.append(np.var(a))

    return variances


if __name__ == "__main__":
    print("--- Weight Initialization Variance Simulation ---")

    # 20-layer network with layer width of 100
    layers = [100] + [100] * 20

    # 1. Naive Small Scale (0.01) with Tanh
    vars_naive_small = run_deep_network(layers, "naive_small", "tanh")
    print(f"\nNaive Small (scale=0.01) + Tanh:")
    print(f"  Layer 0 Variance:  {vars_naive_small[0]:.6f}")
    print(f"  Layer 5 Variance:  {vars_naive_small[5]:.6e}")
    print(f"  Layer 20 Variance: {vars_naive_small[20]:.6e}")
    assert vars_naive_small[20] < 1e-15, "Naive small should vanish to zero!"

    # 2. Naive Large Scale (1.0) with Tanh
    vars_naive_large = run_deep_network(layers, "naive_large", "tanh")
    print(f"\nNaive Large (scale=1.0) + Tanh:")
    print(f"  Layer 0 Variance:  {vars_naive_large[0]:.6f}")
    print(f"  Layer 5 Variance:  {vars_naive_large[5]:.6f}")
    print(f"  Layer 20 Variance: {vars_naive_large[20]:.6f}")

    # 3. Xavier Glorot Normal with Tanh
    vars_xavier = run_deep_network(layers, "xavier", "tanh")
    print(f"\nXavier (Glorot) Normal + Tanh:")
    print(f"  Layer 0 Variance:  {vars_xavier[0]:.6f}")
    print(f"  Layer 5 Variance:  {vars_xavier[5]:.6f}")
    print(f"  Layer 20 Variance: {vars_xavier[20]:.6f}")
    # Xavier keeps variance stable around 0.02 without completely vanishing
    assert (
        vars_xavier[20] > 0.01
    ), "Xavier should prevent activations from vanishing!"

    # 4. He Normal with ReLU
    vars_he = run_deep_network(layers, "he", "relu")
    print(f"\nHe (Kaiming) Normal + ReLU:")
    print(f"  Layer 0 Variance:  {vars_he[0]:.6f}")
    print(f"  Layer 5 Variance:  {vars_he[5]:.6f}")
    print(f"  Layer 20 Variance: {vars_he[20]:.6f}")
    # He Normal keeps variance stable for ReLU activations without vanishing
    assert vars_he[20] > 0.1, "He Normal should prevent ReLU from vanishing!"

    # 5. Xavier Normal with ReLU (Highlighting Failure Case)
    vars_xavier_relu = run_deep_network(layers, "xavier", "relu")
    print(f"\nXavier (Glorot) Normal + ReLU (Failure Case):")
    print(f"  Layer 0 Variance:  {vars_xavier_relu[0]:.6f}")
    print(f"  Layer 5 Variance:  {vars_xavier_relu[5]:.6f}")
    print(f"  Layer 20 Variance: {vars_xavier_relu[20]:.6e}")
    # Xavier variance drops by 1/2 on every layer under ReLU, vanishing by layer 20
    assert (
        vars_xavier_relu[20] < 1e-3
    ), "Xavier should fail (vanish) when paired with ReLU!"

    print("\n  [PASS] All initialization variance bounds verified successfully.")
