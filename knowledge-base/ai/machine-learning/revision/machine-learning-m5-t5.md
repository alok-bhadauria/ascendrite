# Ascendrite Revision Layer: Enterprise MLOps & Serving Pipelines

## 1. Uniform Quantization Math

### Affine Scaling & Zero-Point
Quantizes a real value $r \in [r_{\min}, r_{\max}]$ to an integer $q \in [q_{\min}, q_{\max}]$:

$$S = \frac{r_{\max} - r_{\min}}{q_{\max} - q_{\min}}$$
$$Z = \operatorname{round}\left( \frac{-r_{\min}}{S} \right) + q_{\min}$$

*   **Quantize:** $q = \operatorname{clamp}\left( \operatorname{round}\left( \frac{r}{S} \right) + Z, q_{\min}, q_{\max} \right)$
*   **Dequantize:** $\hat{r} = S \cdot (q - Z)$

### PTQ vs. QAT
*   **PTQ:** Fits scale $S$ and zero-point $Z$ after training using calibration data (KL-divergence or min-max).
*   **QAT:** Quantizes weights during the forward pass. Backpropagation uses the **Straight-Through Estimator (STE)** to bypass the zero rounding derivative:
    $$\frac{\partial L}{\partial w} \approx \frac{\partial L}{\partial \hat{w}} \quad \text{where } \hat{w} = D(Q(w))$$

---

## 2. Serving Engine Optimization

### Graph Compilation (ONNX)
*   **Operator Fusion:** Collapses sequential graph operations (e.g. `Conv2D` + `BatchNorm` + `ReLU`) into a single fused GPU kernel call.
*   **Constant Folding:** Computes static parts of the computational graph during compile time.

### Triton Inference Server
*   **Dynamic Batching:** Delays individual inference calls by a tiny window (e.g. `max_queue_delay_microseconds: 5000`) to stack requests into a larger batch, maximizing tensor core utilization.
*   **Ensembles:** Routes data in-memory between preprocess, inference, and postprocess steps to reduce network/IPC serialization cost.

---

## 3. Drift Monitoring Metrics

### Population Stability Index (PSI)
Compares proportions of baseline (actual) samples $A_b$ against target (expected/new) samples $T_b$ over $B$ bins:

$$\text{PSI} = \sum_{b=1}^B (T_b - A_b) \cdot \ln\left( \frac{T_b}{A_b} \right)$$

*   **Interpretation:**
    *   $\text{PSI} < 0.1$: Distribution is stable.
    *   $0.1 \le \text{PSI} < 0.25$: Moderate drift. Alert triggered.
    *   $\text{PSI} \ge 0.25$: Significant drift. Retraining required.

### Kolmogorov-Smirnov (KS) Test
Determines if baseline samples and target samples come from the same continuous distribution by evaluating cumulative ECDFs $F_{1, n}$ and $F_{2, m}$:

$$D_{n, m} = \sup_{x} \left| F_{1, n}(x) - F_{2, m}(x) \right|$$

*   **Drift Trigger:** Reject null hypothesis if $D_{n, m} > c(\alpha) \sqrt{\frac{n + m}{n \cdot m}}$.
