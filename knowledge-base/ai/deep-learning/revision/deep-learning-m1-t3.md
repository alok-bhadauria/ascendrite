# Ascendrite Revision Layer: Loss Functions

## 1. Regression & Likelihood

### Mean Squared Error (MSE)
$$\mathcal{L}_{\text{MSE}} = \frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2$$

*   **Statistical Foundation:** Derived from Maximum Likelihood Estimation (MLE) under the assumption of additive Gaussian noise $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$ on targets.
*   **Outlier Sensitivity:** Penalizes errors quadratically, rendering the optimization highly sensitive to out-of-distribution outliers.

---

## 2. Classification & Cross-Entropy

### Binary Cross-Entropy (BCE)
$$\mathcal{L}_{\text{BCE}} = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln(\hat{y}_i) + (1 - y_i) \ln(1 - \hat{y}_i) \right]$$

*   **Statistical Foundation:** Derived from MLE under Bernoulli target distributions $P(Y=y_i) = \hat{y}_i^{y_i}(1-\hat{y}_i)^{1-y_i}$.

### Categorical Cross-Entropy (CCE)
$$\mathcal{L}_{\text{CCE}} = -\frac{1}{N} \sum_{i=1}^N \sum_{c=1}^K y_{ic} \ln(\hat{y}_{ic})$$

*   **Statistical Foundation:** Derived from MLE under Multinomial target distributions $P(Y=y_i) = \prod_c \hat{y}_{ic}^{y_{ic}}$ using one-hot encoded targets.

---

## 3. Information Theory & KL Divergence

### Kullback-Leibler (KL) Divergence
Measures difference between true distribution $P$ and approximation $Q$:

$$D_{\text{KL}}(P \parallel Q) = \sum_{x} P(x) \ln\left( \frac{P(x)}{Q(x)} \right)$$

### Key Identities
*   **Cross-Entropy Connection:**
    $$H(P, Q) = H(P) + D_{\text{KL}}(P \parallel Q)$$
    Since Shannon Entropy $H(P)$ is constant for fixed labels, minimizing Cross-Entropy $H(P, Q)$ is mathematically equivalent to minimizing the KL divergence $D_{\text{KL}}(P \parallel Q)$.
*   **Asymmetry:** $D_{\text{KL}}(P \parallel Q) \neq D_{\text{KL}}(Q \parallel P)$
    *   *Forward KL* ($D_{\text{KL}}(P \parallel Q)$): Mean-seeking, zero-avoiding. $Q(x) > 0$ wherever $P(x) > 0$.
    *   *Reverse KL* ($D_{\text{KL}}(Q \parallel P)$): Mode-seeking, zero-forcing. Focuses on local modes, $Q(x) = 0$ wherever $P(x) = 0$ is acceptable.
