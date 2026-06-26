# Ascendrite Interview Prep: Mixed Precision & Mixed Training

## Q1: Compare FP16 and BF16 in terms of bit layout, exponent/fraction sizes, dynamic ranges, and practical training stability.

### Standard Answer
**1. Bit Layout and Range:**
*   **FP16 (Half Precision):** Allocates 1 sign bit, 5 exponent bits, and 10 fraction (mantissa) bits.
    *   *Minimum positive value:* $\approx 6 \times 10^{-5}$
    *   *Maximum value:* $65,504$
    *   *Risk:* The narrow 5-bit exponent range leads to frequent underflows (small gradients become 0) and overflows (large activations become Inf/NaN).
*   **BF16 (Brain Floating Point):** Allocates 1 sign bit, 8 exponent bits, and 7 fraction (mantissa) bits.
    *   *Minimum positive value:* $\approx 1.2 \times 10^{-38}$
    *   *Maximum value:* $\approx 3.4 \times 10^{38}$
    *   *Benefit:* Because it shares the 8-bit exponent width of FP32, it has the same dynamic range. This prevents underflow and overflow, making it highly stable.

**2. Precision vs. Stability:**
*   **FP16** has higher precision (10 fraction bits $\approx 3.3$ decimal digits) than **BF16** (7 fraction bits $\approx 2.1$ decimal digits).
*   However, in deep learning, **numerical range (stability) is far more critical than high precision**. If activations/gradients underflow or overflow, training fails. Therefore, BF16 is significantly more stable and does not require complex loss scaling, making it the preferred format on modern GPUs.

---

## Q2: What is 'Loss Scaling' in FP16 mixed precision training? Why is it needed, and how does the dynamic loss scaling algorithm adjust the scale factor?

### Standard Answer
In FP16 training, gradients often become very small. Because FP16 cannot represent values below $6 \times 10^{-5}$, these small gradients underflow to exactly zero, stopping weight updates.

**Mechanism:**
1.  **Scaling:** Before backpropagation, we multiply the loss $J$ by a scale factor $S$ (e.g., $1024$):
    $$J_{\text{scaled}} = S \cdot J$$
    By the chain rule, this scales all gradients by $S$, shifting them into the representable range of FP16.
2.  **Unscaling:** Before updating the parameter weights, we divide the gradients by $S$ to restore their original scales:
    $$\mathbf{g}_{\text{unscaled}} = \frac{\mathbf{g}_{\text{scaled}}}{S}$$

**Dynamic Scaling Algorithm:**
If $S$ is too large, gradients will overflow to infinity (Inf), creating NaNs. If $S$ is too small, gradients will underflow.
*   **Initialization:** Start with a large scale factor $S$ (e.g., $65,536$).
*   **Gradient Check:** After backpropagation, scan the gradients for NaN or Inf values.
*   **Overflow Action:** If any NaN/Inf is detected, discard the entire step (do not update weights) and reduce the scale factor:
    $$S \leftarrow S \cdot 0.5$$
*   **Normal Action:** If gradients are clean, unscale them, convert them to FP32, and update weights.
*   **Scale Expansion:** If no overflow occurs for $N$ consecutive steps (e.g. 2000 steps), increase the scale factor:
    $$S \leftarrow S \cdot 2.0$$

---

## Q3: In mixed precision training, why must we maintain a copy of the weights in FP32 (the 'master weights') for the optimizer update?

### Standard Answer
Maintaining FP32 master weights is necessary to prevent small gradient updates from being lost to underflow during parameter updates.

Let's examine the gradient update step:
$$\mathbf{W}^{(t+1)} = \mathbf{W}^{(t)} - \eta \mathbf{g}$$

In deep learning:
*   The learning rate $\eta$ is often small (e.g., $10^{-4}$).
*   The gradient values $\mathbf{g}$ are also small.
*   The update product $\eta \mathbf{g}$ is extremely small (e.g., $10^{-6}$ or smaller).

If we store the weights $\mathbf{W}$ in FP16 format:
1.  **Precision Limit:** FP16 has only 10 bits of fraction. If the weight value $\mathbf{W}^{(t)}$ is relatively large (e.g., $1.0$) and the update $\eta \mathbf{g}$ is small (e.g., $10^{-6}$), the ratio of the update to the weight is below the machine epsilon of FP16 ($\approx 9.7 \times 10^{-4}$).
2.  **Underflow:** The addition of the small value has no numerical effect, and the weight remains exactly unchanged:
    $$\mathbf{W}^{(t)} - \eta \mathbf{g} = \mathbf{W}^{(t)} \quad \text{in FP16}$$
    The model stops learning entirely.
3.  **FP32 Solution:** By maintaining the weights in FP32 (which has 23 fraction bits and a machine epsilon of $\approx 1.29 \times 10^{-7}$), we can accumulate these tiny updates stably. The master weights are updated in FP32 and then cast to FP16 for the next forward pass.
