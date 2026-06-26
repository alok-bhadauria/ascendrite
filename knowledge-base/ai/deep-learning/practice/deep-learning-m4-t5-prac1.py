import numpy as np


def compute_attention_context(
    scores: np.ndarray, H_enc: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Computes attention weights and aggregates the context vector.

    Args:
        scores: Raw alignment scores of shape (Tx, 1)
        H_enc: Encoder states of shape (h, Tx)

    Returns:
        tuple containing:
            - c_t: Context vector of shape (h, 1)
            - alphas: Normalized attention weights of shape (Tx, 1)
    """
    # 1. Compute softmax over scores
    exp_scores = np.exp(scores - np.max(scores))
    alphas = exp_scores / np.sum(exp_scores)

    # 2. Compute context vector as weighted sum of H_enc
    c_t = np.dot(H_enc, alphas)

    return c_t, alphas


if __name__ == "__main__":
    print("--- Running Attention Context Practice ---")

    # Dimensions: Tx=3, h=2
    scores = np.array([[2.0], [0.0], [1.0]])
    H_enc = np.array(
        [[1.0, 2.0, 3.0],
         [4.0, 0.0, -1.0]]
    )

    c_t, alphas = compute_attention_context(scores, H_enc)
    print("Alphas:\n", alphas)
    print("Context Vector:\n", c_t)

    # Manual calculations:
    # exp = [exp(2), exp(0), exp(1)] = [7.3890561, 1.0, 2.71828183]
    # sum = 11.10733793
    # alphas = [0.66524, 0.09003, 0.24473]
    expected_alphas = np.array([[np.exp(2)], [1.0], [np.exp(1)]]) / (np.exp(2) + 1.0 + np.exp(1))
    assert np.allclose(alphas, expected_alphas)

    # c_t[0] = 1*alpha_0 + 2*alpha_1 + 3*alpha_2 = 0.66524 + 0.18006 + 0.73419 = 1.57949
    # c_t[1] = 4*alpha_0 + 0 - 1*alpha_2 = 4*0.66524 - 0.24473 = 2.41623
    expected_c_t = np.dot(H_enc, expected_alphas)
    assert np.allclose(c_t, expected_c_t)
    print("Attention weight normalization and context aggregation verified.")

    print("\n  [PASS] Attention context practice verified.")
