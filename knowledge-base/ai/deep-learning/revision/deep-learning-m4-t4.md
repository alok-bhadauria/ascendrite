# Ascendrite Revision Card: Gated Recurrent Units (GRU)

## GRU vs. LSTM Architectures

*   **State Space:** Collapses LSTM's dual states ($\mathbf{c}_t, \mathbf{h}_t$) into a single hidden state $\mathbf{h}_t$.
*   **Gate Count:** Uses only 2 gates (reset, update) instead of 3 gates in LSTM.
*   **Parameter Footprint:** Uses ~25% fewer parameters than an LSTM of the same hidden dimension, yielding faster training and lower memory requirements.

## Mathematical Equations

At step $t$, given input $\mathbf{x}_t$ and previous hidden state $\mathbf{h}_{t-1}$:

1.  **Reset Gate ($\mathbf{r}_t$):** Filters what past context should be ignored when computing new candidate state updates:
    $$\mathbf{r}_t = \sigma(\mathbf{W}_{xr} \mathbf{x}_t + \mathbf{W}_{hr} \mathbf{h}_{t-1} + \mathbf{b}_r)$$
2.  **Update Gate ($\mathbf{z}_t$):** Regulates how much of the old state to keep versus how much of the new candidate to write (acts as combined forget-input gates):
    $$\mathbf{z}_t = \sigma(\mathbf{W}_{xz} \mathbf{x}_t + \mathbf{W}_{hz} \mathbf{h}_{t-1} + \mathbf{b}_z)$$
3.  **Candidate Hidden State ($\tilde{\mathbf{h}}_t$):** Computes new candidate values. Note that reset gate modulates the previous state *before* weight multiplication:
    $$\tilde{\mathbf{h}}_t = \tanh(\mathbf{W}_{xh} \mathbf{x}_t + \mathbf{r}_t \odot (\mathbf{W}_{hh} \mathbf{h}_{t-1}) + \mathbf{b}_h)$$

## State Interpolation & Gradient Flow

*   **Hidden State Update:** Linear interpolation between previous hidden state and candidate state:
    $$\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$$
*   **Vanishing Gradient Solution:** The step derivative contains the additive term $(1 - \mathbf{z}_t)$. If the network keeps the update gate closed ($1 - \mathbf{z}_t \approx 1.0$), gradients flow directly back over time.
