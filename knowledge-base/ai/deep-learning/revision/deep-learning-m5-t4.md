# Ascendrite Revision Card: Mixed Precision & Mixed Training

## Numerical Bit Layouts

*   **FP32:** 1 sign, 8 exponent, 23 fraction bits. Standard training precision.
*   **FP16:** 1 sign, 5 exponent, 10 fraction bits. Range is restricted: $[6 \times 10^{-5}, 65504]$. Narrow range leads to gradient underflow and overflow.
*   **BF16:** 1 sign, 8 exponent, 7 fraction bits. Matches the dynamic range of FP32, preventing underflow. BF16 has lower precision (7 fraction bits) but is highly stable.

## Master Weights & Precision Preservation

*   **Master Weights copy:** Parameter weights are stored and updated in FP32. Forward and backward activation passes are run in FP16/BF16. Small updates would underflow if accumulated in FP16.

## Loss Scaling Mathematics

*   **Underflow:** Gradients below $6 \times 10^{-5}$ drop to 0 in FP16.
*   **Scaling:** Multiply the loss by a scaling factor $S$ (e.g. 1024) before backpropagation, shifting gradients into representable range:
    $$\mathbf{g}_{\text{scaled}} = S \cdot \mathbf{g}$$
*   **Unscaling:** Divide gradients by $S$ before optimizer updates:
    $$\mathbf{g}_{\text{unscaled}} = \frac{\mathbf{g}_{\text{scaled}}}{S}$$

## Dynamic Scaling Protocol

1.  Initialize scale factor $S$ to a large value (e.g. 65536).
2.  Multiply loss by $S$, compute backpropagation.
3.  **Check for overflow:** If gradients contain NaN or Inf:
    *   Discard the optimizer step.
    *   Scale down: $S \leftarrow S \cdot 0.5$.
4.  If gradients are clean (no NaNs/Infs) for $N$ consecutive steps:
    *   Scale up: $S \leftarrow S \cdot 2.0$.
5.  *Note:* BF16 has the same exponent width as FP32, so it does not require loss scaling.
