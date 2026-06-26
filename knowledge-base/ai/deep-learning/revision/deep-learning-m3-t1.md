# Ascendrite Revision Layer: CNN Foundations

## 1. Image Representation & Parameters

*   **Grayscale Image:** $2D$ shape tensor: $(H, W)$ of pixel intensity values.
*   **RGB Image:** $3D$ shape tensor: $(C, H, W)$ where $C = 3$ channels (Red, Green, Blue).
*   **Intermediate Features:** Represented as $(C_{\text{in}}, H, W)$ where $C_{\text{in}}$ is the number of input filters/channels.
*   **Parameter Count Reduction:** CNNs enforce local receptive fields and weight sharing to drastically reduce model capacity and prevent parameter explosion compared to fully connected MLPs.

---

## 2. Convolution & Cross-Correlation Math

*   **2D Cross-Correlation (Framework 'Convolution'):**
    $$S(i, j) = \sum_{m=0}^{K_H-1} \sum_{n=0}^{K_W-1} I(i + m, j + n) K(m, n)$$
*   **2D Convolution (Mathematical definition with flipped kernel):**
    $$S(i, j) = \sum_{m=0}^{K_H-1} \sum_{n=0}^{K_W-1} I(i - m, j - n) K(m, n)$$
*   **Multi-Channel input:** A kernel is a 3D tensor of shape $(C_{\text{in}}, K_H, K_W)$. The 2D outputs from each input channel are summed to produce a single feature map:
    $$Z(h, w) = \sum_{c=1}^{C_{\text{in}}} \sum_{m=0}^{K_H-1} \sum_{n=0}^{K_W-1} X(c, h + m, w + n) K(c, m, n) + b$$
*   **Weight dimensions for $C_{\text{out}}$ output channels:**
    $$\mathbf{W} \in \mathbb{R}^{C_{\text{out}} \times C_{\text{in}} \times K_H \times K_W}$$

---

## 3. Spatial Dimension Formula

Given input dimensions ($H_{\text{in}}, W_{\text{in}}$), kernel size ($K_H, K_W$), padding ($P_H, P_W$), and stride ($S_H, S_W$), the output spatial size is calculated as:
$$H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} - K_H + 2P_H}{S_H} \right\rfloor + 1$$
$$W_{\text{out}} = \left\lfloor \frac{W_{\text{in}} - K_W + 2P_W}{S_W} \right\rfloor + 1$$

### Common Configurations:
*   **Valid Convolution (No Padding):** $P=0, S=1$:
    $$H_{\text{out}} = H_{\text{in}} - K_H + 1$$
*   **Same Convolution (Preserves Spatial Dimension):** $S=1$, padding is set as:
    $$P = \frac{K - 1}{2} \quad \text{(for odd kernel size } K\text{)}$$
    resulting in $H_{\text{out}} = H_{\text{in}}$ and $W_{\text{out}} = W_{\text{in}}$.
