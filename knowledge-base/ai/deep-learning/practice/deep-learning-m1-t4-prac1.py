import numpy as np


def compute_gradients_and_update(
    x: np.ndarray,
    y: np.ndarray,
    W1: np.ndarray,
    b1: np.ndarray,
    W2: np.ndarray,
    b2: np.ndarray,
    lr: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    """Performs a single step of forward pass, backward pass, and parameter updates

    for a 2-layer MLP with ReLU activation in the hidden layer and linear activation
    in the output layer, using Mean Squared Error loss.

    Dimensions:
    - x: (input_dim, 1)
    - y: (output_dim, 1)
    - W1: (hidden_dim, input_dim)
    - b1: (hidden_dim, 1)
    - W2: (output_dim, hidden_dim)
    - b2: (output_dim, 1)

    Returns:
    - Updated W1, b1, W2, b2, and the scalar loss.
    """
    # 1. Forward Pass
    z1 = W1 @ x + b1
    a1 = np.maximum(0.0, z1)  # ReLU
    z2 = W2 @ a1 + b2
    a2 = z2  # Linear activation at output

    # Loss computation
    loss = 0.5 * np.sum((a2 - y) ** 2)

    # 2. Backward Pass
    # delta2 = dJ/dz2 = (a2 - y)
    delta2 = a2 - y

    # Output gradients
    dW2 = delta2 @ a1.T
    db2 = delta2

    # Hidden delta: delta1 = (W2.T @ delta2) * relu_deriv(z1)
    delta1 = (W2.T @ delta2) * (z1 > 0).astype(float)

    # Hidden gradients
    dW1 = delta1 @ x.T
    db1 = delta1

    # 3. Parameter Updates (SGD)
    W1_updated = W1 - lr * dW1
    b1_updated = b1 - lr * db1
    W2_updated = W2 - lr * dW2
    b2_updated = b2 - lr * db2

    return W1_updated, b1_updated, W2_updated, b2_updated, loss
