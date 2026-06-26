# Ascendrite Interview Prep: Weight Initialization

## Q1: Prove mathematically that initializing all weights in an MLP to a constant value $c$ prevents the network from learning diverse features.

### Standard Answer
Consider a hidden layer $l$ containing $d_l$ neurons, taking inputs from layer $l-1$ containing $d_{l-1}$ units. The pre-activation of neuron $i$ in layer $l$ is:
$$z_i^{(l)} = \sum_{j=1}^{d_{l-1}} W_{ij}^{(l)} a_j^{(l-1)} + b_i^{(l)}$$
If all weights are initialized to a constant $W_{ij}^{(l)} = c$ and biases are zero:
$$z_i^{(l)} = c \sum_{j=1}^{d_{l-1}} a_j^{(l-1)}$$
Since this sum is identical for every neuron $i$, we establish that the pre-activations are identical: $z_1^{(l)} = z_2^{(l)} = \dots = z_{d_l}^{(l)} = z^{(l)}$. The post-activation outputs are also identical: $a_i^{(l)} = f(z_i^{(l)}) = f(z^{(l)}) = a^{(l)}$ for all $i$.

During the backward pass, the error delta for neuron $i$ in a hidden layer $l < L$ is:
$$\delta_i^{(l)} = \left( \sum_{k=1}^{d_{l+1}} W_{ki}^{(l+1)} \delta_k^{(l+1)} \right) f^{\prime}(z_i^{(l)})$$
Since all weights at layer $l+1$ are initialized to $c$, and all outputs of layer $l+1$ (and thus error terms $\delta_k^{(l+1)}$) are identical, let $\delta_k^{(l+1)} = \delta^{(l+1)}$. The error term simplifies to:
$$\delta_i^{(l)} = \left( \sum_{k=1}^{d_{l+1}} c \cdot \delta^{(l+1)} \right) f^{\prime}(z^{(l)}) = d_{l+1} c \cdot \delta^{(l+1)} f^{\prime}(z^{(l)}) = \delta^{(l)}$$
Since $\delta_i^{(l)}$ is identical for all $i$, the gradient with respect to the weight $W_{ij}^{(l)}$ is:
$$\frac{\partial J}{\partial W_{ij}^{(l)}} = \delta_i^{(l)} a_j^{(l-1)} = \delta^{(l)} a_j^{(l-1)}$$
This gradient is independent of the destination neuron index $i$. Consequently, the updated weights will remain identical across all destination neurons:
$$W_{ij}^{(l) \text{ new}} = c - \eta \delta^{(l)} a_j^{(l-1)}$$
Since $W_{ij}^{(l) \text{ new}}$ is equal for all $i$, the weights remain symmetric. The neurons are locked in a symmetric state, making it impossible for them to specialize in learning different features.

---

## Q2: Derive the forward pass variance matching condition for Xavier (Glorot) Initialization.

### Standard Answer
Consider a linear layer output $z = \sum_{i=1}^{n_{\text{in}}} w_i x_i$. We make the following assumptions:
1.  The weights $w_i$ are i.i.d. random variables with mean $E[w_i] = 0$ and variance $\operatorname{Var}(w)$.
2.  The inputs $x_i$ are i.i.d. random variables with mean $E[x_i] = 0$ and variance $\operatorname{Var}(x)$.
3.  $w_i$ and $x_i$ are mutually independent.

We compute the variance of $z$:
$$\operatorname{Var}(z) = \operatorname{Var}\left( \sum_{i=1}^{n_{\text{in}}} w_i x_i \right)$$
Since the terms $w_i x_i$ are independent, the variance of the sum is the sum of the variances:
$$\operatorname{Var}(z) = \sum_{i=1}^{n_{\text{in}}} \operatorname{Var}(w_i x_i)$$
Applying the product variance formula:
$$\operatorname{Var}(w_i x_i) = E[w_i]^2 \operatorname{Var}(x_i) + E[x_i]^2 \operatorname{Var}(w_i) + \operatorname{Var}(w_i)\operatorname{Var}(x_i)$$
Since $E[w_i] = 0$ and $E[x_i] = 0$:
$$\operatorname{Var}(w_i x_i) = \operatorname{Var}(w_i)\operatorname{Var}(x_i) = \operatorname{Var}(w)\operatorname{Var}(x)$$
Substituting this back into the sum:
$$\operatorname{Var}(z) = \sum_{i=1}^{n_{\text{in}}} \operatorname{Var}(w)\operatorname{Var}(x) = n_{\text{in}} \operatorname{Var}(w)\operatorname{Var}(x)$$

To keep the scale of activations stable across layers, we want $\operatorname{Var}(z) = \operatorname{Var}(x)$, which requires:
$$n_{\text{in}} \operatorname{Var}(w) = 1 \implies \operatorname{Var}(w) = \frac{1}{n_{\text{in}}}$$
This ensures the forward activation scale is preserved.

---

## Q3: Why does Xavier initialization fail in networks with ReLU activations, and how does He (Kaiming) initialization resolve this mathematically?

### Standard Answer
**1. Xavier Failure on ReLU:**
Xavier initialization assumes the activation function $f$ is linear with unit derivative near zero ($f(z) = z$), meaning $\operatorname{Var}(a^{(l)}) \approx \operatorname{Var}(z^{(l)})$. 

However, the Rectified Linear Unit (ReLU) activation function is defined as $a = \max(0, z)$. If $z$ is symmetrically distributed about zero (with mean 0), ReLU zeros out exactly half the distribution. The second moment of the post-activation output becomes:
$$E[a^2] = \int_{0}^{\infty} z^2 p(z) dz = \frac{1}{2} \int_{-\infty}^{\infty} z^2 p(z) dz = \frac{1}{2} \operatorname{Var}(z)$$
Since $a \ge 0$, the mean $E[a]$ is non-zero, but we trace the variance expansion. The activation variance at layer $l$ is:
$$\operatorname{Var}(z^{(l)}) = \left( \frac{1}{2} n_{l-1} \operatorname{Var}(w^{(l)}) \right) \operatorname{Var}(z^{(l-1)})$$
If we use Xavier initialization ($\\operatorname{Var}(w^{(l)}) = \frac{1}{n_{l-1}}$), the recurrence relation becomes:
$$\operatorname{Var}(z^{(l)}) = \frac{1}{2} \operatorname{Var}(z^{(l-1)})$$
On each layer, the variance of the activations is halved. In a network with $L$ layers, the variance of the final activations shrinks by a factor of $(1/2)^L$. For deep networks (e.g. $L = 50$), the activations vanish to zero, stopping learning.

**2. He Initialization Correction:**
He initialization corrects this by doubling the target variance to compensate for the half-zeroing of ReLU:
$$\frac{1}{2} n_{l-1} \operatorname{Var}(w^{(l)}) = 1 \implies \operatorname{Var}(w^{(l)}) = \frac{2}{n_{l-1}}$$
Using this scale ($W \sim \mathcal{N}(0, 2/n_{\text{in}})$) keeps the activation scale perfectly stable regardless of depth.
