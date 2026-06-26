# Ascendrite Revision Card: Long Short-Term Memory (LSTM)

## Dual-State Architecture

*   **Cell State ($\mathbf{c}_t$):** Long-term memory highway running linearly down the temporal steps.
*   **Hidden State ($\mathbf{h}_t$):** Short-term working memory, computed by filtering the cell state.

## Mathematical Gate Equations

At step $t$, given input $\mathbf{x}_t$ and previous state $\mathbf{h}_{t-1}$:

1.  **Forget Gate ($\mathbf{f}_t$):** Decides what information to discard from the previous cell state.
    $$\mathbf{f}_t = \sigma(\mathbf{W}_{xf} \mathbf{x}_t + \mathbf{W}_{hf} \mathbf{h}_{t-1} + \mathbf{b}_f)$$
2.  **Input Gate ($\mathbf{i}_t$):** Decides what new features to write to the cell state.
    $$\mathbf{i}_t = \sigma(\mathbf{W}_{xi} \mathbf{x}_t + \mathbf{W}_{hi} \mathbf{h}_{t-1} + \mathbf{b}_i)$$
3.  **Candidate Cell ($\tilde{\mathbf{c}}_t$):** Computes new candidate values.
    $$\tilde{\mathbf{c}}_t = \tanh(\mathbf{W}_{xc} \mathbf{x}_t + \mathbf{W}_{hc} \mathbf{h}_{t-1} + \mathbf{b}_c)$$
4.  **Output Gate ($\mathbf{o}_t$):** Filters what updated cell memory to expose.
    $$\mathbf{o}_t = \sigma(\mathbf{W}_{xo} \mathbf{x}_t + \mathbf{W}_{ho} \mathbf{h}_{t-1} + \mathbf{b}_o)$$

## State Updates & Gradient Highway

*   **Cell State Update:** Element-wise combination of forget gate and input gate modulation:
    $$\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t$$
*   **Hidden State Update:** Output gate filters the activated cell state:
    $$\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t)$$
*   **Vanishing Gradient Solution:** The derivative of $\mathbf{c}_t$ with respect to $\mathbf{c}_{t-1}$ contains the additive term $\mathbf{f}_t$. If the network learns to keep the forget gate open ($\mathbf{f}_t \approx 1.0$), gradients flow backward without decaying exponentially.

## Best Practices

*   **Forget Gate Bias:** Initialize $\mathbf{b}_f$ to a high value (e.g. $1.0$ or $2.0$) at the start of training to keep forget gates open initially, preventing early gradient vanishing.
*   **Activations:** Gates must use sigmoid $\sigma$ to output probabilities $[0, 1]$. Memory updates must use $\tanh$ to allow positive and negative offsets $[-1, 1]$.
