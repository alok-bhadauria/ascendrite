# Ascendrite Revision Layer: Anomaly Detection & Time Series

## 1. Isolation Forest Anomaly Scoring

Anomalies isolate faster (shorter path lengths) under random splits.

*   **Average BST Path Length ($c(N)$):**
    $$c(N) = 2 \ln(N - 1) + 0.5772156649 - \frac{2(N - 1)}{N}$$
*   **Anomaly Score ($s(\mathbf{x}, N)$):**
    $$s(\mathbf{x}, N) = 2^{-\frac{\mathbb{E}[h(\mathbf{x})]}{c(N)}}$$
    *   $\mathbb{E}[h(\mathbf{x})] \to 0 \implies s \to 1$ (definite anomaly).
    *   $\mathbb{E}[h(\mathbf{x})] \to c(N) \implies s \to 0.5$ (typical sample).

---

## 2. One-Class SVM & Autoencoders

### One-Class SVM (Origin Separation)
$$\min_{\mathbf{w}, \xi, \rho} \frac{1}{2} \|\mathbf{w}\|_2^2 + \frac{1}{\nu N} \sum_{i=1}^N \xi_i - \rho \quad \text{subject to} \quad \mathbf{w}^{\top} \Phi(\mathbf{x}_i) \ge \rho - \xi_i, \quad \xi_i \ge 0$$
*   **$\nu$ (Nu):** Upper bound on outlier fraction, lower bound on support vector fraction.

### Autoencoders (Reconstruction Loss)
*   **Reconstruction Error:** $e_i = \|\mathbf{x}_i - \hat{\mathbf{x}}_i\|_2^2$.
*   **Threshold:** Fit Autoencoder strictly on normal data. Anomalies yield high reconstruction error. Set threshold using extreme percentiles (e.g. 99th percentile of normal error).

---

## 3. Time Series & ARIMA

### Weak Stationarity
1.  Constant Mean: $\mathbb{E}[Y_t] = \mu$
2.  Constant Variance: $\text{Var}(Y_t) = \sigma^2$
3.  Constant Autocovariance: $\text{Cov}(Y_t, Y_{t-k}) = \gamma_k$ (independent of $t$).

### Augmented Dickey-Fuller (ADF) Test
Unit root test of autoregressive models:
*   $H_0$: $\gamma = 0$ (unit root exists, non-stationary).
*   $H_1$: $\gamma < 0$ (stationary).

### ARIMA(p, d, q) Formulation
$$W_t = c + \sum_{i=1}^p \phi_i W_{t-i} + \epsilon_t + \sum_{j=1}^q \theta_j \epsilon_{t-j}$$
where $W_t = \Delta^d Y_t$ is the differenced series, $\phi_i$ are AR parameters, and $\theta_j$ are MA parameters.
*   *Anomaly Detection:* Flag when $|Y_t - \hat{Y}_t| > \text{threshold}$.
