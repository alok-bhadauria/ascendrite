# Ascendrite Interview Prep: CNN Architectures

## Q1: Why does stacking multiple $3 \times 3$ convolutional layers perform better than using a single larger convolutional layer (like $7 \times 7$)? Prove parameter efficiency.

### Standard Answer
Stacking multiple small convolutional layers instead of using a single large one provides two main benefits: parameter efficiency and increased non-linearity.

**1. Receptive Field Equivalence:**
A receptive field is the local input region that affects a specific output activation. 
*   One layer of $3 \times 3$ convolution with stride 1 looks at a $3 \times 3$ patch.
*   A second $3 \times 3$ layer looks at a $3 \times 3$ patch of the first layer, which corresponds to a $5 \times 5$ patch of the input.
*   A third $3 \times 3$ layer looks at a $3 \times 3$ patch of the second layer, which maps to a $7 \times 7$ patch of the input.
Thus, three $3 \times 3$ layers have the same effective receptive field as a single $7 \times 7$ layer.

**2. Parameter Count Proof:**
Let $C$ be the number of input and output channels.
*   **Single $7 \times 7$ layer parameters:**
    $$\text{Params}_{7 \times 7} = 7 \times 7 \times C \times C = 49C^2$$
*   **Three $3 \times 3$ layers parameters:**
    $$\text{Params}_{3 \times 3} = 3 \times (3 \times 3 \times C \times C) = 27C^2$$
This represents a reduction of parameters by:
    $$\frac{49C^2 - 27C^2}{49C^2} \approx 44.9\%$$
Fewer parameters reduce memory usage and control overfitting.

**3. Increased Non-linearity:**
Three stacked layers include three activation functions (e.g. ReLU) instead of a single activation function, allowing the network to learn more complex features.

---

## Q2: Provide a mathematical proof showing how ResNet skip connections prevent vanishing gradients.

### Standard Answer
Let a network block be represented as:
$$x_{l+1} = x_l + F(x_l, W_l)$$
Where $x_l$ is the input to the $l$-th residual block, $F$ represents the residual mapping, and $W_l$ represents the weights.

By recursively applying this relation from layer $l$ to a deeper layer $L$:
$$x_L = x_l + \sum_{i=l}^{L-1} F(x_i, W_i)$$
This formulation shows that any deeper layer state $x_L$ is the sum of the earlier state $x_l$ plus the accumulated residuals.

During backpropagation, let $J$ be the scalar loss. By the chain rule, the gradient of the loss with respect to the input $x_l$ is:
$$\frac{\partial J}{\partial x_l} = \frac{\partial J}{\partial x_L} \frac{\partial x_L}{\partial x_l} = \frac{\partial J}{\partial x_L} \left( I + \frac{\partial}{\partial x_l} \sum_{i=l}^{L-1} F(x_i, W_i) \right)$$

This expression shows that the gradient $\frac{\partial J}{\partial x_l}$ is split into two terms:
1.  **Identity Pathway:** $\frac{\partial J}{\partial x_L} \cdot I$, which passes the gradient directly back without matrix multiplications.
2.  **Residual Pathway:** $\frac{\partial J}{\partial x_L} \left( \frac{\partial}{\partial x_l} \sum_{i=l}^{L-1} F(x_i, W_i) \right)$.

Even if the gradient through the residual pathway vanishes (e.g., if weights are near zero or activations saturate), the identity term $I$ ensures that the total gradient $\frac{\partial J}{\partial x_l}$ never vanishes. Gradients from the output can flow directly back to the very first layers.

---

## Q3: What is the difference between an Identity Shortcut and a Projection Shortcut in ResNet? Write down the equation for the projection shortcut.

### Standard Answer
*   **Identity Shortcut:** When the input $x$ and the residual function output $F(x)$ share the same spatial dimensions (height and width) and channel depth, we add them directly:
    $$y = F(x) + x$$
*   **Projection Shortcut:** When spatial sizes change (due to strides) or the number of channels increases inside a residual block, direct addition is not defined. We must project the input $x$ to match the shape of $F(x)$:
    $$y = F(x) + W_s x$$
    Where $W_s$ is a projection parameter.
*   **Implementation:** In practice, $W_s$ is implemented using a $1 \times 1$ convolution layer with:
    1.  Stride equal to the spatial downsampling stride of the block (e.g. 2) to scale down height and width.
    2.  Number of kernels equal to the output channel depth of the block to scale up the channel dimension.
