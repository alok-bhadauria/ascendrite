import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Computes the Sigmoid activation function.

    Formula:
        sigma(z) = 1 / (1 + exp(-z))
    """
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


def sigmoid_derivative(z: np.ndarray) -> np.ndarray:
    """Computes the derivative of the Sigmoid activation function.

    Formula:
        sigma'(z) = sigma(z) * (1 - sigma(z))
    """
    s = sigmoid(z)
    return s * (1.0 - s)


def tanh(z: np.ndarray) -> np.ndarray:
    """Computes the Hyperbolic Tangent (Tanh) activation function.

    Formula:
        tanh(z) = (exp(z) - exp(-z)) / (exp(z) + exp(-z))
    """
    return np.tanh(z)


def tanh_derivative(z: np.ndarray) -> np.ndarray:
    """Computes the derivative of the Tanh activation function.

    Formula:
        tanh'(z) = 1 - tanh(z)^2
    """
    t = tanh(z)
    return 1.0 - t**2


def compute_saturation_ratio(
    z: np.ndarray, activation_type: str = "sigmoid", threshold: float = 1e-2
) -> float:
    """Computes the fraction of neurons in a layer that are saturated.

    A neuron is considered saturated if the absolute value of its activation
    derivative is below the specified threshold, which indicates that gradients
    will vanish during backpropagation.

    Args:
        z: Pre-activation array of arbitrary shape.
        activation_type: The activation function type ('sigmoid' or 'tanh').
        threshold: The threshold below which a derivative is considered
          saturated.

    Returns:
        float: The ratio of saturated neurons in range [0, 1].
    """
    if activation_type.lower() == "sigmoid":
        derivs = sigmoid_derivative(z)
    elif activation_type.lower() == "tanh":
        derivs = tanh_derivative(z)
    else:
        raise ValueError(
            f"Unsupported activation type for saturation analysis: '{activation_type}'"
        )

    # Count elements where the derivative is below the threshold
    saturated_count = np.sum(np.abs(derivs) < threshold)
    total_count = z.size

    return float(saturated_count / total_count)
