# Ascendrite Revision Layer: CNN Layers

## 1. Max Pooling vs. Average Pooling

Pooling downsamples activation grids to reduce computation and control overfitting:
*   **Max Pooling:** Selects the maximum value in the sliding window:
    $$y(h, w) = \max_{m,n} X(h \cdot S_H + m, w \cdot S_W + n)$$
    *   **Behavior:** Acts as a dominant feature detector (retaining peaks, edges, strong activations). Introduces local translation invariance.
*   **Average Pooling:** Computes the mean value in the window:
    $$y(h, w) = \frac{1}{K_H \cdot K_W} \sum_{m,n} X(h \cdot S_H + m, w \cdot S_W + n)$$
    *   **Behavior:** Smooths out features, acting as a low-pass filter.
*   **Parameter Count:** Pooling layers contain zero learnable weights or biases.

---

## 2. Dimensionality & Channel Invariance

*   **Channel Invariance:** Pooling is applied independently to each channel. If the input shape is $(C, H_{\text{in}}, W_{\text{in}})$, the output shape is $(C, H_{\text{out}}, W_{\text{out}})$. The channel depth $C$ is preserved.
*   **Spatial Dimensions:**
    $$H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} - K_H + 2P_H}{S_H} \right\rfloor + 1$$
    $$W_{\text{out}} = \left\lfloor \frac{W_{\text{in}} - K_W + 2P_W}{S_W} \right\rfloor + 1$$
    For standard $2 \times 2$ pooling with a stride of 2 (no padding), output spatial height/width are exactly halved: $H_{\text{out}} = H_{\text{in}} / 2$.

---

## 3. The Flattening Layer

Bridges 3D convolutional activation tensors to 1D dense layers.
*   **Operation:** Reshapes the 3D tensor $(C, H, W)$ into a 1D vector of shape $(C \cdot H \cdot W, 1)$:
    $$\mathbf{x}_{\text{flatten}} = \operatorname{reshape}(\mathbf{X}_{\text{feature}}, [C \cdot H \cdot W, 1])$$
*   **Trade-off:**
    *   **Pros:** Necessary to feed standard classifier heads.
    *   **Cons:** Discards spatial coordinates. Geometric neighborhood coordinates are lost.
