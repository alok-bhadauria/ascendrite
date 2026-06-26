# Ascendrite Interview Prep: Activation Functions

## Q1: Derive the derivative of the Sigmoid activation function. Discuss how its mathematical limits contribute to the vanishing gradient problem in deep neural networks.

### Standard Answer
The Sigmoid function is defined as:
$$\sigma(z) = \frac{1}{1 + e^{-z}} = (1 + e^{-z})^{-1}$$

#### 1. Derivation of the Derivative
Applying the power rule and the chain rule:
$$\sigma'(z) = -(1 + e^{-z})^{-2} \cdot \frac{d}{dz}(1 + e^{-z}) = -(1 + e^{-z})^{-2} \cdot (-e^{-z}) = \frac{e^{-z}}{(1 + e^{-z})^2}$$
We can rewrite this expression by factorizing:
$$\sigma'(z) = \left( \frac{1}{1 + e^{-z}} \right) \cdot \left( \frac{e^{-z}}{1 + e^{-z}} \right)$$
Since $1 - \sigma(z) = 1 - \frac{1}{1 + e^{-z}} = \frac{1 + e^{-z} - 1}{1 + e^{-z}} = \frac{e^{-z}}{1 + e^{-z}}$, we substitute this back:
$$\sigma'(z) = \sigma(z)(1 - \sigma(z))$$

#### 2. Vanishing Gradient Relationship
*   The function $\sigma(z)$ is bounded between $0$ and $1$. The product $\sigma(z)(1 - \sigma(z))$ reaches its maximum value when $\sigma(z) = 0.5$, which occurs at $z = 0$.
*   At $z=0$, the derivative is $\sigma'(0) = 0.5 \cdot (1 - 0.5) = 0.25$.
*   For any other value of $z$, the derivative is strictly less than $0.25$.
*   During backpropagation, the gradient is multiplied by the activation derivative at each layer:
    $$\frac{\partial L}{\partial \mathbf{x}^{(l-1)}} = \mathbf{W}^{(l)\top} \left( \frac{\partial L}{\partial \mathbf{z}^{(l)}} \odot f'(\mathbf{z}^{(l)}) \right)$$
    If $f = \sigma$, each layer scales the incoming gradient by at most $0.25$. In a 5-layer network, the gradient flowing to the first layer is scaled by at least $0.25^5 \approx 0.00097$, leading to vanishing gradients that prevent the early layers from learning.

---

## Q2: What is the 'dying ReLU' problem, and how do Leaky ReLU and Parametric ReLU (PReLU) address it mathematically?

### Standard Answer
The **dying ReLU** problem is a failure mode where a neuron becomes permanently inactive and outputs zero for all training inputs, preventing its parameters from updating.

#### 1. The Cause of Dying ReLU
The standard ReLU activation is $f(z) = \max(0, z)$. Its derivative is $f'(z) = 0$ for $z < 0$. 
During training, if a large gradient update shifts a neuron's weights and bias such that its pre-activation $z = \mathbf{w}^{\top}\mathbf{x} + b$ is negative for all inputs in the training dataset, then:
*   $f(z) = 0$ for the entire dataset (zero activation).
*   $f'(z) = 0$ for all backpropagation updates, yielding $\frac{\partial L}{\partial \mathbf{w}} = 0$ and $\frac{\partial L}{\partial b} = 0$.
*   Because the gradients are zero, the weights and bias can never change, locking the neuron in a permanently dead state.

#### 2. Mitigation via Leaky ReLU and PReLU
Both variants introduce a non-zero slope for the negative region, keeping gradients active:
*   **Leaky ReLU:** Assigns a fixed, small positive slope $\alpha \approx 0.01$:
    $$f(z) = \max(\alpha z, z)$$
    $$f'(z) = \begin{cases} 1 & \text{if } z > 0 \\ \alpha & \text{if } z < 0 \end{cases}$$
    Since $\alpha > 0$, the gradient is never zero, allowing dead neurons to recover and adapt their weights.
*   **Parametric ReLU (PReLU):** Generalizes Leaky ReLU by making the slope $\alpha$ a learnable parameter:
    $$f(z) = \max(\alpha_i z, z)$$
    where $\alpha_i$ is updated via gradient descent for channel $i$:
    $$\frac{\partial L}{\partial \alpha_i} = \sum_{j} \frac{\partial L}{\partial f(z_j)} \cdot \frac{\partial f(z_j)}{\partial \alpha_i} = \sum_{j: z_j < 0} \frac{\partial L}{\partial f(z_j)} \cdot z_j$$
    This allows the network to learn whether a particular layer should behave symmetrically, as a standard ReLU, or as a linear activation.

---

## Q3: Prove the translation-invariance property of the Softmax activation function, and explain how this property is used to prevent numerical overflow in execution graphs.

### Standard Answer
The Softmax function converts a logit vector $\mathbf{z} \in \mathbb{R}^K$ to a probability vector $\mathbf{a} \in \mathbb{R}^K$:
$$a_i = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

#### 1. Proof of Translation Invariance
Let $c \in \mathbb{R}$ be a scalar constant. Adding $c$ to every element of $\mathbf{z}$ yields the vector $\mathbf{z} + c\mathbf{1}$. Evaluating the Softmax for index $i$:
$$\operatorname{softmax}(\mathbf{z} + c\mathbf{1})_i = \frac{e^{z_i + c}}{\sum_{j=1}^K e^{z_j + c}}$$
Using exponential multiplication rules ($e^{a+b} = e^a \cdot e^b$):
$$\operatorname{softmax}(\mathbf{z} + c\mathbf{1})_i = \frac{e^c \cdot e^{z_i}}{\sum_{j=1}^K e^c \cdot e^{z_j}}$$
Factoring out the constant term $e^c$ from the summation in the denominator:
$$\operatorname{softmax}(\mathbf{z} + c\mathbf{1})_i = \frac{e^c \cdot e^{z_i}}{e^c \cdot \sum_{j=1}^K e^{z_j}} = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}} = \operatorname{softmax}(\mathbf{z})_i$$
This completes the proof.

#### 2. Prevention of Numerical Overflow
In 32-bit single-precision floating-point arithmetic (FP32), values larger than $\approx 88.7$ cause $e^z$ to overflow to positive infinity (`inf`).
*   To prevent this during runtime execution, we compute the maximum value of the logit vector:
    $$M = \max_{j} z_j$$
*   We subtract $M$ from all logits, setting $c = -M$. The shifted logit vector is $\tilde{\mathbf{z}} = \mathbf{z} - M\mathbf{1}$.
*   Because we subtract the maximum value, every shifted logit is non-positive:
    $$\tilde{z}_i \le 0 \quad \forall i$$
*   The maximum value in $\tilde{\mathbf{z}}$ is exactly $0.0$, making the maximum exponentiated value $e^0 = 1.0$. This guarantees that no term in the Softmax calculation can exceed $1.0$, preventing floating-point overflow while maintaining mathematically identical probability outputs.
