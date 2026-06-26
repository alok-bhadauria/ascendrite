# Ascendrite Interview Prep: CNN Foundations

## Q1: Explain the mathematical and conceptual differences between cross-correlation and convolution, and why deep learning libraries choose cross-correlation.

### Standard Answer
**1. Mathematical Difference:**
For a 2D image $I$ and kernel $K$ of size $M \times N$, the operations are formulated as:
*   **Cross-Correlation:**
    $$(I \star K)(i, j) = \sum_{m=0}^{M-1} \sum_{n=0}^{N-1} I(i + m, j + n) K(m, n)$$
*   **Convolution:**
    $$(I * K)(i, j) = \sum_{m=0}^{M-1} \sum_{n=0}^{N-1} I(i - m, j - n) K(m, n)$$

Mathematically, convolution flips the kernel both horizontally and vertically before performing the element-wise multiplication and summation. Flipping is necessary to satisfy the commutative property of convolution ($I * K = K * I$), which is vital in mathematical analysis and Fourier transform proofs. Cross-correlation is not commutative.

**2. Deep Learning Implementation Choice:**
In deep learning networks, the elements of the kernel $K$ are weights that are learned from scratch during training. If we implemented true convolution, the network would simply learn a flipped version of the weights to achieve the exact same output. Flipping the kernel is an unnecessary computational overhead. Thus, frameworks like PyTorch and TensorFlow implement cross-correlation in their 2D convolutional layers, but retain the name 'convolution' by convention.

---

## Q2: Derive the general spatial dimensionality formula for a 1D convolution, and explain where the floor function arises.

### Standard Answer
Let the input dimension be $W$, kernel size be $K$, padding be $P$, and stride be $S$.

1.  **Padding Extension:** Adding padding $P$ symmetrically to both sides increases the effective width of the input to:
    $$W_{\text{padded}} = W + 2P$$
2.  **Valid Scanning Range:** When the sliding kernel is placed at the very first position (touching the left edge), its right edge reaches index $K$. The remaining distance the kernel can slide is:
    $$W_{\text{padded}} - K = W + 2P - K$$
3.  **Stride Discretization:** The kernel slides along this remaining distance in steps of size $S$. The number of complete steps it can take is:
    $$\frac{W + 2P - K}{S}$$
4.  **Adding the First Step:** Since the initial position itself produces one output pixel, the total number of output pixels is:
    $$W_{\text{out}} = \frac{W + 2P - K}{S} + 1$$
5.  **The Floor Function:** If the stride $S$ does not divide the remaining distance perfectly, the kernel cannot perform a full step at the end. Since we cannot perform operations on partial input windows, we discard the remaining pixels by applying the floor function:
    $$W_{\text{out}} = \left\lfloor \frac{W + 2P - K}{S} \right\rfloor + 1$$

---

## Q3: If a convolutional layer has an input tensor of shape $(N, 64, 56, 56)$ and applies 128 kernels of shape $3 \times 3$ with a stride of 2 and padding of 1:
1.  **What is the shape of the output tensor?**
2.  **How many parameters (weights and biases) does this layer contain?**

### Standard Answer
**1. Output Shape Calculation:**
The input dimensions are $H_{\text{in}} = 56$, $W_{\text{in}} = 56$. The kernel size is $K = 3$, stride is $S = 2$, and padding is $P = 1$.
Using the dimension formula:
$$H_{\text{out}} = \left\lfloor \frac{56 - 3 + 2(1)}{2} \right\rfloor + 1 = \left\lfloor \frac{55}{2} \right\rfloor + 1 = 27 + 1 = 28$$
Since the input is square and parameters are symmetric, $W_{\text{out}} = 28$.
The number of output channels is equal to the number of filters: $C_{\text{out}} = 128$.
Thus, the output tensor shape is:
$$(N, 128, 28, 28)$$

**2. Parameter Count Calculation:**
*   Each of the 128 filters must match the input channel depth ($C_{\text{in}} = 64$).
*   The shape of a single weight kernel is $(C_{\text{in}}, K_H, K_W) = (64, 3, 3)$.
*   Number of weights in one filter: $64 \times 3 \times 3 = 576$ parameters.
*   Total weights for all 128 filters: $128 \times 576 = 73,728$ parameters.
*   Each of the 128 filters has 1 learnable bias parameter, adding 128 bias parameters.
*   Total parameter count:
    $$\text{Total Parameters} = 73,728 \text{ (weights)} + 128 \text{ (biases)} = 73,856 \text{ parameters}$$
