import numpy as np


def compute_mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Computes the Mean Squared Error (MSE) loss.

    Formula:
        loss = (1 / N) * sum((y_true - y_pred)^2)
    """
    return float(np.mean((y_true - y_pred) ** 2))


def compute_mse_gradient(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Computes the gradient of the MSE loss with respect to predictions.

    Formula:
        d_loss/d_ypred = (2 / N) * (y_pred - y_true)
    """
    n = y_true.size
    return (2.0 / n) * (y_pred - y_true)


def compute_bce_logits(y_true: np.ndarray, logits: np.ndarray) -> float:
    """Computes numerically stable Binary Cross-Entropy loss from logits.

    Formula:
        loss = (1 / N) * sum(max(logits, 0) - y_true * logits + ln(1 + exp(-|logits|)))
    """
    loss = np.maximum(logits, 0.0) - y_true * logits + np.log(1.0 + np.exp(-np.abs(logits)))
    return float(np.mean(loss))


def compute_bce_logits_gradient(y_true: np.ndarray, logits: np.ndarray) -> np.ndarray:
    """Computes the gradient of stable BCE loss with respect to logits.

    Formula:
        d_loss/d_logits = (1 / N) * (sigmoid(logits) - y_true)
    """
    n = y_true.size
    # Compute Sigmoid: 1 / (1 + exp(-logits))
    sig = 1.0 / (1.0 + np.exp(-np.clip(logits, -500, 500)))
    return (sig - y_true) / n
