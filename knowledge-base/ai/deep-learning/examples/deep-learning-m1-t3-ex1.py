import numpy as np


def stable_binary_cross_entropy(z: np.ndarray, y: np.ndarray) -> float:
    """Computes stable BCE loss from pre-activation logits z.

    Formula:
        loss = max(z, 0) - y * z + ln(1 + exp(-|z|))
    """
    # Computes element-wise stable loss
    loss = np.maximum(z, 0.0) - y * z + np.log(1.0 + np.exp(-np.abs(z)))
    return float(np.mean(loss))


def stable_categorical_cross_entropy(logits: np.ndarray, y_onehot: np.ndarray) -> float:
    """Computes stable Categorical Cross-Entropy from logits using Log-Softmax.

    Formula:
        log_softmax_i = z_i - max(z) - ln(sum(exp(z_j - max(z))))
        loss = - sum(y_i * log_softmax_i)
    """
    # Subtract max logit for translation invariance stability
    max_logits = np.max(logits, axis=1, keepdims=True)
    shifted_logits = logits - max_logits
    
    # Compute log sum exp
    log_sum_exp = np.log(np.sum(np.exp(shifted_logits), axis=1, keepdims=True))
    log_softmax = shifted_logits - log_sum_exp
    
    # CCE = -mean(sum(y * log_softmax))
    loss = -np.sum(y_onehot * log_softmax, axis=1)
    return float(np.mean(loss))


def discrete_kl_divergence(p: np.ndarray, q: np.ndarray, epsilon: float = 1e-9) -> float:
    """Computes the KL divergence D_KL(P || Q) for discrete distributions.

    Adds epsilon to avoid log(0) issues.
    """
    p_norm = p / np.sum(p)
    q_norm = q / np.sum(q)
    
    # Clip values to prevent log(0)
    q_norm = np.clip(q_norm, epsilon, 1.0)
    
    # Compute sum(P * ln(P / Q))
    with np.errstate(divide='ignore', invalid='ignore'):
        terms = p_norm * np.log(np.where(p_norm > 0, p_norm / q_norm, 1.0))
    return float(np.sum(terms))


if __name__ == "__main__":
    # --- 1. Stable BCE Verification ---
    print("--- 1. Stable BCE Verification ---")
    # Logits: one large positive, one large negative, one near zero
    logits_bce = np.array([20.0, -20.0, 0.0])
    targets_bce = np.array([1.0, 0.0, 1.0])
    
    # Standard computation would yield nan/inf due to exp(20) or log(0)
    # Stable computation evaluates successfully
    bce_loss = stable_binary_cross_entropy(logits_bce, targets_bce)
    print(f"Logits:  {logits_bce}")
    print(f"Targets: {targets_bce}")
    print(f"Stable BCE Loss: {bce_loss:.6f}")

    # --- 2. Stable CCE Verification ---
    print("\n--- 2. Stable CCE Verification ---")
    logits_cce = np.array([
        [1000.0, 999.0, 998.0],
        [-100.0, -100.0, 0.0]
    ])
    # One-hot targets: class 0 for sample 1, class 2 for sample 2
    targets_cce = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0]
    ])
    
    cce_loss = stable_categorical_cross_entropy(logits_cce, targets_cce)
    print("Logits matrix (with extreme scale variations):\n", logits_cce)
    print(f"Stable CCE Loss: {cce_loss:.6f}")

    # --- 3. KL Divergence Asymmetry Demonstration ---
    print("\n--- 3. KL Divergence Asymmetry Demonstration ---")
    # True distribution P is bimodal (peaks at index 1 and 8)
    P = np.array([0.05, 0.4, 0.05, 0.0, 0.0, 0.0, 0.05, 0.4, 0.05])
    
    # Q1 is a broad distribution covering both modes (Mean-seeking / Forward KL fit)
    Q1 = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2])
    
    # Q2 is a sharp distribution focused on a single mode (Mode-seeking / Reverse KL fit)
    Q2 = np.array([0.0, 0.8, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1])
    
    print("True distribution P: ", P)
    print("Broad approx Q1:     ", Q1)
    print("Single mode approx Q2:", Q2)
    
    # Compute Forward KL: D_KL(P || Q)
    kl_p_q1 = discrete_kl_divergence(P, Q1)
    kl_p_q2 = discrete_kl_divergence(P, Q2)
    
    # Compute Reverse KL: D_KL(Q || P)
    kl_q1_p = discrete_kl_divergence(Q1, P)
    kl_q2_p = discrete_kl_divergence(Q2, P)
    
    print(f"\nForward KL Divergence D_KL(P || Q):")
    print(f"  P || Q1 (Broad):       {kl_p_q1:.6f}  (Preferred by Forward KL)")
    print(f"  P || Q2 (Single Mode): {kl_p_q2:.6f}  (High penalty due to zero values at mode 2)")
    
    print(f"\nReverse KL Divergence D_KL(Q || P):")
    print(f"  Q1 || P (Broad):       {kl_q1_p:.6f}")
    print(f"  Q2 || P (Single Mode): {kl_q2_p:.6f}  (Preferred by Reverse KL / Zero-forcing)")
