# Ascendrite Revision Layer: Weight Initialization

## 1. The Necessity of Symmetry Breaking

Initializing weights to zero or any constant value ($c$) results in identical outputs and gradients for all neurons in the same layer:
*   **Result:** Every neuron in a given layer computes the exact same activation value: $a_i^{(l)} = a_j^{(l)}$.
*   **Backpropagation:** Every weight $W_{ij}^{(l)}$ receives the same gradient update direction: $\frac{\partial J}{\partial W_{ij}^{(l)}} = \delta^{(l)} a_j^{(l-1)}$.
*   **Implication:** Neurons are locked in a symmetric state, meaning they learn the exact same features. The layer acts as if it has a width of 1, collapsing the representation capacity.
*   **Solution:** Initialize weights randomly to break this mathematical symmetry.

---

## 2. Xavier (Glorot) Initialization (Linear & Tanh)

Maintains constant variance of activations and gradients across layers under the assumption of linear activation functions.
*   **Target Variance:**
    $$\operatorname{Var}(w) = \frac{2}{n_{\text{in}} + n_{\text{out}}}$$
*   **Xavier Normal:** Weights are drawn from a normal distribution:
    $$W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}} + n_{\text{out}}}\right)$$
*   **Xavier Uniform:** Weights are drawn from a uniform distribution:
    $$W_{ij} \sim U(-r, r) \quad \text{where } r = \sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}$$

---

## 3. He (Kaiming) Initialization (ReLU)

Adapts the variance targets to account for the asymmetric zero-clipping of ReLU activation functions, which halves the signal variance on every layer.
*   **Target Variance:**
    $$\operatorname{Var}(w) = \frac{2}{n_{\text{in}}}$$
*   **He Normal:** Weights are drawn from a normal distribution:
    $$W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}}}\right)$$
*   **He Uniform:** Weights are drawn from a uniform distribution:
    $$W_{ij} \sim U(-r, r) \quad \text{where } r = \sqrt{\frac{6}{n_{\text{in}}}}$$
