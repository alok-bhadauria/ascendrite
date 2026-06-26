# Ascendrite Revision Card: CNN Architectures

## Evolutions: LeNet-5, AlexNet, and VGG

*   **LeNet-5:** Foundation of CNNs. Used large $5 \times 5$ convolutions, average pooling, and sigmoid activations. Optimized for small inputs like digits.
*   **AlexNet:** Scaled CNNs. Introduced **ReLU** to prevent saturation, dropout to reduce overfitting, and overlapping max pooling.
*   **VGG:** Introduced uniform architecture. Replaced large kernels with stacks of small $3 \times 3$ kernels. Stacking three $3 \times 3$ layers matches the receptive field of one $7 \times 7$ layer, but uses fewer parameters ($27C^2$ vs. $49C^2$) and includes more non-linear activations.

## Residual Networks (ResNet)

*   **The Problem:** Deep networks (20+ layers) suffered from optimization degradation where accuracy saturated or dropped due to vanishing gradients during backpropagation.
*   **Residual Learning:** Instead of learning $H(x)$, learn $F(x) = H(x) - x$. The output block is:
    $$y = F(x) + x$$
*   **Gradient Flow Proof:** Applying the chain rule:
    $$\frac{\partial J}{\partial x} = \frac{\partial J}{\partial y} \left( \frac{\partial F(x)}{\partial x} + I \right)$$
    The addition of the identity matrix $I$ ensures that even if the gradient through the residual layers $\frac{\partial F(x)}{\partial x}$ approaches zero, the total gradient never vanishes.

## Dimension Matching & Projection Shortcuts

*   **Identity Shortcuts:** Used when input shape matches output shape:
    $$y = F(x) + x$$
*   **Projection Shortcuts:** Used when spatial size or channel count changes across a block. We project the input $x$ to match the dimension of $F(x)$ using a projection matrix $W_s$:
    $$y = F(x) + W_s x$$
*   **Implementation:** In practice, $W_s$ is a $1 \times 1$ convolution with a stride of 2 (if downsampling spatial resolution) and output channels equal to the residual channels.
