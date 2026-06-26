import numpy as np


def luong_attention_forward(
    s_t: np.ndarray, H_enc: np.ndarray, W_a: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Computes the forward pass of Luong multiplicative attention.

    Args:
        s_t: Decoder hidden state at step t, shape (h, 1)
        H_enc: Encoder hidden states, shape (h, Tx) where Tx is sequence length
        W_a: Weight parameter matrix of shape (h, h)

    Returns:
        tuple containing:
            - c_t: Context vector of shape (h, 1)
            - alphas: Attention weights of shape (Tx, 1)
    """
    # 1. Compute alignment scores: score = s_t^T * W_a * h_i
    # W_a_H shape: (h, Tx)
    W_a_H = np.dot(W_a, H_enc)
    # scores shape: (Tx, 1)
    scores = np.dot(W_a_H.T, s_t)

    # 2. Normalize using softmax to get attention weights
    # Subtract max for numerical stability
    exp_scores = np.exp(scores - np.max(scores))
    alphas = exp_scores / np.sum(exp_scores)

    # 3. Compute context vector: sum_i alpha_i * h_i
    # c_t shape: (h, 1)
    c_t = np.dot(H_enc, alphas)

    return c_t, alphas


if __name__ == "__main__":
    print("--- Running Luong Multiplicative Attention Verification ---")
    np.random.seed(42)

    h, Tx = 3, 4  # 3 features, 4 encoder steps
    s_t = np.array([[1.0], [0.0], [-1.0]])  # Decoder state
    H_enc = np.array(
        [[1.0, 0.0, -1.0, 0.5],
         [0.0, 2.0, 1.0, -0.5],
         [0.5, 0.0, 0.5, 1.0]]
    )
    W_a = np.array(
        [[0.5, 0.0, 0.1],
         [0.1, 0.2, 0.0],
         [0.0, 0.0, 0.4]]
    )

    c_t, alphas = luong_attention_forward(s_t, H_enc, W_a)
    print("Attention Weights (alphas):\n", alphas)
    print("Context Vector (c_t):\n", c_t)

    assert alphas.shape == (Tx, 1)
    assert c_t.shape == (h, 1)
    assert np.isclose(np.sum(alphas), 1.0)

    # Manual alignment calculations check:
    # W_a * H_enc = [ [0.55, 0.0, -0.45, 0.35],
    #                 [0.1,  0.4,  0.1,   0.05],
    #                 [0.2,  0.0,  0.2,   0.4] ]
    # score_0 = s_t^T * column_0 = 1*0.55 + 0 + -1*0.2 = 0.35
    # score_1 = s_t^T * column_1 = 1*0.0 + 0 + 0 = 0.0
    # score_2 = s_t^T * column_2 = 1*-0.45 + 0 + -1*0.2 = -0.65
    # score_3 = s_t^T * column_3 = 1*0.35 + 0 + -1*0.4 = -0.05
    #
    # exp = [exp(0.35), exp(0.0), exp(-0.65), exp(-0.05)] = [1.41906755, 1.0, 0.52204578, 0.95122942]
    # sum_exp = 3.89234275
    # alphas = [0.36458, 0.25691, 0.13412, 0.24438]
    expected_alphas = np.array([[0.36457788], [0.2569147], [0.13412123], [0.24438619]])
    assert np.allclose(alphas, expected_alphas)
    print("Attention weights match manual calculation.")

    # Context vector check: H_enc * alphas
    # c_t[0] = 1*0.36457788 + 0 - 1*0.13412123 + 0.5*0.24438619 = 0.352649745
    expected_c_t_0 = 0.352649745
    assert np.isclose(c_t[0, 0], expected_c_t_0)
    print("Context vector values match manual calculation.")

    print("\n  [PASS] Luong attention forward pass verified.")
