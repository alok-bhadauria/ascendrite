import numpy as np


class ResidualBlockNumPy:
    """Simulates a residual block with identity and projection pathways in NumPy."""

    def __init__(self, c_in: int, c_out: int, downsample: bool = False):
        self.c_in = c_in
        self.c_out = c_out
        self.downsample = downsample

        # Mock weights for the residual path: F(X) = W2 * ReLU(W1 * X)
        # Using flat arrays for simplicity of mathematical demonstration
        self.W1 = np.random.randn(c_out, c_in) * 0.1
        self.W2 = np.random.randn(c_out, c_out) * 0.1

        # Mock weights for projection path if dimensions mismatch
        if self.downsample or c_in != c_out:
            self.W_proj = np.random.randn(c_out, c_in) * 0.1
        else:
            self.W_proj = None

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, dict]:
        """Forward pass.

        Args:
            X: Input of shape (c_in, N) where N is spatial/batch size

        Returns:
            tuple containing:
                - Output of shape (c_out, N)
                - Cache dictionary
        """
        # 1. Residual path: F(X) = W2 * ReLU(W1 * X)
        z1 = np.dot(self.W1, X)
        a1 = np.maximum(0, z1)  # ReLU
        F_out = np.dot(self.W2, a1)

        # 2. Shortcut path
        if self.W_proj is not None:
            # Projection mapping
            shortcut = np.dot(self.W_proj, X)
        else:
            # Identity mapping
            shortcut = X

        # 3. Addition
        out = F_out + shortcut

        cache = {"X": X, "z1": z1, "a1": a1, "F_out": F_out, "shortcut": shortcut}
        return out, cache

    def backward(self, dY: np.ndarray, cache: dict) -> tuple[np.ndarray, dict]:
        """Backward pass to derive gradients.

        Args:
            dY: Incoming gradients of shape (c_out, N)
            cache: Cache dictionary from forward pass

        Returns:
            tuple containing:
                - dX: Gradient of loss with respect to input X (c_in, N)
                - dW: Dictionary of weight gradients
        """
        X = cache["X"]
        z1 = cache["z1"]
        a1 = cache["a1"]

        # Gradients through residual path: F(X) = W2 * a1
        # dF_out is identical to dY since Y = F_out + shortcut
        dF_out = dY
        dW2 = np.dot(dF_out, a1.T)
        da1 = np.dot(self.W2.T, dF_out)

        # Gradient through ReLU
        dz1 = da1 * (z1 > 0)
        dW1 = np.dot(dz1, X.T)
        dX_residual = np.dot(self.W1.T, dz1)

        # Gradient through shortcut path
        if self.W_proj is not None:
            dX_shortcut = np.dot(self.W_proj.T, dY)
            dW_proj = np.dot(dY, X.T)
        else:
            dX_shortcut = dY
            dW_proj = None

        # Total input gradient: addition of pathways
        dX = dX_residual + dX_shortcut

        grads = {"dW1": dW1, "dW2": dW2}
        if dW_proj is not None:
            grads["dW_proj"] = dW_proj

        return dX, grads


if __name__ == "__main__":
    print("--- Running ResNet Skip Connection Verification ---")
    np.random.seed(42)

    # 1. Verification of Identity block (c_in == c_out)
    block_id = ResidualBlockNumPy(c_in=4, c_out=4)
    X = np.random.randn(4, 5)

    out_id, cache_id = block_id.forward(X)
    dY = np.random.randn(4, 5)
    dX_id, grads_id = block_id.backward(dY, cache_id)

    # Prove gradient propagation:
    # If we zero out the weights in the residual path, the gradient should flow
    # unchanged through the shortcut (identity path). Let's test this.
    block_zero = ResidualBlockNumPy(c_in=4, c_out=4)
    block_zero.W1.fill(0.0)
    block_zero.W2.fill(0.0)

    out_zero, cache_zero = block_zero.forward(X)
    # Output must equal input exactly (identity shortcut)
    assert np.allclose(out_zero, X)

    dX_zero, _ = block_zero.backward(dY, cache_zero)
    # Gradient must equal outgoing gradient exactly (identity path)
    assert np.allclose(dX_zero, dY)
    print("Identity block gradient flow check passed.")

    # 2. Verification of Projection block (c_in != c_out)
    block_proj = ResidualBlockNumPy(c_in=4, c_out=8)
    out_proj, cache_proj = block_proj.forward(X)
    assert out_proj.shape == (8, 5)
    print("Projection block forward shape verified:", out_proj.shape)

    dY_proj = np.random.randn(8, 5)
    dX_proj, grads_proj = block_proj.backward(dY_proj, cache_proj)
    assert dX_proj.shape == (4, 5)
    assert grads_proj["dW_proj"].shape == (8, 4)
    print("Projection block backward shapes verified.")

    print("\n  [PASS] ResNet skip connection examples verified.")
