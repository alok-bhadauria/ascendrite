# Ascendrite Revision Layer: Backpropagation Calculus

## 1. Vector Chain Rule & Intermediate Error ($\boldsymbol{\delta}^{(l)}$)

For a scalar loss function $J$, we define the error vector (delta) of layer $l$ as:
$$\boldsymbol{\delta}^{(l)} = \frac{\partial J}{\partial \mathbf{z}^{(l)}} \in \mathbb{R}^{d_l}$$

Applying the chain rule recursively:
*   **Output Layer ($L$):**
    $$\boldsymbol{\delta}^{(L)} = \frac{\partial J}{\partial \mathbf{a}^{(L)}} \odot f^{(L)\prime}(\mathbf{z}^{(L)})$$
    where $\odot$ is the Hadamard (element-wise) product and $f^{(L)\prime}(\mathbf{z}^{(L)})$ is the derivative of the activation function at the output layer.
*   **Hidden Layers ($l < L$):**
    $$\boldsymbol{\delta}^{(l)} = \left( \mathbf{W}^{(l+1)\top} \boldsymbol{\delta}^{(l+1)} \right) \odot f^{(l)\prime}(\mathbf{z}^{(l)})$$
    where $\mathbf{W}^{(l+1)} \in \mathbb{R}^{d_{l+1} \times d_l}$ is the weight matrix of the subsequent layer.

---

## 2. Parameter Gradients

Once $\boldsymbol{\delta}^{(l)}$ is computed, the gradients of $J$ with respect to the weight matrix $\mathbf{W}^{(l)}$ and bias vector $\mathbf{b}^{(l)}$ are:
*   **Weights Gradient:**
    $$\frac{\partial J}{\partial \mathbf{W}^{(l)}} = \boldsymbol{\delta}^{(l)} (\mathbf{a}^{(l-1)})^{\top}$$
    resulting in a matrix of size $d_l \times d_{l-1}$.
*   **Biases Gradient:**
    $$\frac{\partial J}{\partial \mathbf{b}^{(l)}} = \boldsymbol{\delta}^{(l)}$$
    resulting in a vector of size $d_l \times 1$.

---

## 3. Dimensional Verification

To prevent dimension mismatch errors in implementations, verify shapes of all vectors and matrices for a single sample:
*   $\mathbf{a}^{(l-1)} \in \mathbb{R}^{d_{l-1} \times 1}$
*   $\mathbf{z}^{(l)} \in \mathbb{R}^{d_l \times 1}$
*   $\mathbf{W}^{(l)} \in \mathbb{R}^{d_l \times d_{l-1}}$
*   $\mathbf{b}^{(l)} \in \mathbb{R}^{d_l \times 1}$
*   $\boldsymbol{\delta}^{(l)} \in \mathbb{R}^{d_l \times 1}$
*   $\frac{\partial J}{\partial \mathbf{W}^{(l)}} = (d_l \times 1) \times (1 \times d_{l-1}) = d_l \times d_{l-1}$
*   $\frac{\partial J}{\partial \mathbf{b}^{(l)}} = d_l \times 1$
