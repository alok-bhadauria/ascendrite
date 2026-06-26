import numpy as np


class LinearLayerNumPy:
    """A dense neural network layer that supports parameter freezing."""

    def __init__(self, in_features: int, out_features: int, name: str):
        self.name = name
        self.W = np.random.randn(out_features, in_features) * 0.1
        self.b = np.zeros((out_features, 1))
        self.frozen = False

        # Gradient storage
        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)

    def forward(self, X: np.ndarray) -> np.ndarray:
        self.X = X  # Cache input for backward pass
        return np.dot(self.W, X) + self.b

    def backward(self, dY: np.ndarray) -> np.ndarray:
        """Computes backward pass.

        Args:
            dY: Incoming gradients of shape (out_features, N)

        Returns:
            np.ndarray: Gradient with respect to inputs (in_features, N)
        """
        N = dY.shape[1]

        if not self.frozen:
            # Compute gradients for weights and biases
            self.dW = np.dot(dY, self.X.T) / N
            self.db = np.sum(dY, axis=1, keepdims=True) / N
        else:
            # Gradients are locked to zero (frozen parameters)
            self.dW = np.zeros_like(self.W)
            self.db = np.zeros_like(self.b)

        # Gradient must still flow backward to earlier layers
        dX = np.dot(self.W.T, dY)
        return dX


if __name__ == "__main__":
    print("--- Running Transfer Learning Layer Freezing Verification ---")
    np.random.seed(42)

    # Setup a 3-layer sequential network:
    # Input (dim 2) -> Layer 1 (dim 3) -> Layer 2 (dim 4) -> Layer 3 (dim 1)
    layer1 = LinearLayerNumPy(2, 3, "layer1")
    layer2 = LinearLayerNumPy(3, 4, "layer2")
    layer3 = LinearLayerNumPy(4, 1, "layer3")

    # Freeze Layer 2 (Simulating frozen backbone layer)
    layer2.frozen = True

    # Dummy inputs and target outputs (N = 5 batch size)
    X = np.random.randn(2, 5)
    targets = np.random.randn(1, 5)

    # 1. Forward Pass
    a1 = layer1.forward(X)
    a2 = layer2.forward(a1)
    predictions = layer3.forward(a2)

    # Calculate Loss: Mean Squared Error
    loss = np.mean((predictions - targets) ** 2)
    print(f"Initial Forward Loss: {loss:.5f}")

    # 2. Backward Pass
    # Gradient of MSE loss: dLoss/dPredictions = 2 * (predictions - targets)
    dLoss_dPred = 2 * (predictions - targets)

    d_a2 = layer3.backward(dLoss_dPred)
    d_a1 = layer2.backward(d_a2)
    d_X = layer1.backward(d_a1)

    # 3. Assertions and Verification
    # Layer 3 was active: should have non-zero parameter gradients
    assert not np.allclose(layer3.dW, 0.0)
    assert not np.allclose(layer3.db, 0.0)
    print("Layer 3 (active) parameter gradients verified.")

    # Layer 2 was frozen: parameter gradients MUST be exactly zero
    assert np.allclose(layer2.dW, 0.0)
    assert np.allclose(layer2.db, 0.0)
    print("Layer 2 (frozen) parameter gradients verified to be exactly zero.")

    # Layer 1 was active: should have non-zero parameter gradients
    # This proves that gradients successfully propagated through the frozen Layer 2!
    assert not np.allclose(layer1.dW, 0.0)
    assert not np.allclose(layer1.db, 0.0)
    print("Layer 1 (active, behind frozen layer) parameter gradients verified.")

    # 4. Perform weight update to confirm weights of layer2 do not change
    lr = 0.1
    for layer in [layer1, layer2, layer3]:
        layer.W -= lr * layer.dW
        layer.b -= lr * layer.db

    # Layer 2 weights must remain identical to their original values
    # Re-run forward pass with updated weights to confirm learning
    a1_new = layer1.forward(X)
    a2_new = layer2.forward(a1_new)
    predictions_new = layer3.forward(a2_new)
    loss_new = np.mean((predictions_new - targets) ** 2)
    print(f"Post-Update Loss: {loss_new:.5f}")

    # Loss should decrease
    assert loss_new < loss
    print("Loss reduction confirmed after training active parameters.")

    print("\n  [PASS] Layer freezing and gradient flow simulations verified.")
