import numpy as np


def apply_gradients_with_freezing(
    weights: dict[str, np.ndarray],
    grads: dict[str, np.ndarray],
    frozen_keys: list[str],
    lr: float,
) -> dict[str, np.ndarray]:
    """Applies gradient descent updates to weights while enforcing freezing.

    Args:
        weights: Dictionary mapping layer weight names to NumPy arrays
        grads: Dictionary mapping weight names to their calculated gradients
        frozen_keys: List of names of weights that should not be updated
        lr: Learning rate

    Returns:
        dict: Updated weights dictionary
    """
    updated_weights = {}

    for key, W in weights.items():
        if key in frozen_keys:
            # If the weight is frozen, retain original value without updates
            updated_weights[key] = W.copy()
        else:
            # Update trainable weights using gradient descent
            dW = grads.get(key, np.zeros_like(W))
            updated_weights[key] = W - lr * dW

    return updated_weights


if __name__ == "__main__":
    print("--- Running Transfer Learning Practice ---")

    # Initial mock weights dictionary
    weights = {
        "conv1.W": np.array([[1.0, 2.0], [3.0, 4.0]]),
        "conv2.W": np.array([[0.5, -0.5], [1.0, 0.0]]),
        "fc.W": np.array([[1.5, 2.5]]),
    }

    # Mock gradients dictionary
    grads = {
        "conv1.W": np.array([[0.1, 0.2], [0.1, 0.1]]),
        "conv2.W": np.array([[-0.2, 0.1], [0.3, 0.2]]),
        "fc.W": np.array([[0.5, 1.0]]),
    }

    # Case 1: Only freeze backbone convolutions ('conv1.W' and 'conv2.W')
    frozen_keys = ["conv1.W", "conv2.W"]
    lr = 0.1

    new_weights = apply_gradients_with_freezing(weights, grads, frozen_keys, lr)

    # conv1.W and conv2.W should remain unchanged
    assert np.allclose(new_weights["conv1.W"], weights["conv1.W"])
    assert np.allclose(new_weights["conv2.W"], weights["conv2.W"])
    
    # fc.W should be updated: 1.5 - 0.1 * 0.5 = 1.45; 2.5 - 0.1 * 1.0 = 2.40
    expected_fc_W = np.array([[1.45, 2.40]])
    assert np.allclose(new_weights["fc.W"], expected_fc_W)
    print("Case 1 (Feature Extraction update mapping) passed.")

    # Case 2: Full fine-tuning (nothing frozen)
    new_weights_full = apply_gradients_with_freezing(weights, grads, [], lr)
    
    # conv1.W should change: 1.0 - 0.1 * 0.1 = 0.99
    assert not np.allclose(new_weights_full["conv1.W"], weights["conv1.W"])
    print("Case 2 (Full fine-tuning update mapping) passed.")

    print("\n  [PASS] Gradient updates freezing practice verified.")
