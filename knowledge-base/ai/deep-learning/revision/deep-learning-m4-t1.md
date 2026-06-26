# Ascendrite Revision Card: Sequential Data & RNN Foundations

## Constraints of Feedforward Networks (MLPs)

*   **Fixed Dimension Inputs:** Cannot naturally process varying sequence lengths.
*   **Loss of Order:** Flattening processes tokens in isolation and discards the sequence structure.
*   **No Memory State:** Each sample is processed independently without context memory.

## Elman RNN Hidden State

*   **Hidden Memory State ($\mathbf{h}_t$):** Vector summarizing information up to step $t$. Size is a hyperparameter representing representation channels, independent of sequence length $T$.
*   **Recurrent Update Equation:**
    $$\mathbf{h}_t = \tanh(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)$$
    *   $\mathbf{x}_t$: Input vector at step $t$ (embedding size $d$).
    *   $\mathbf{W}_{xh}$: Input-to-hidden weight matrix.
    *   $\mathbf{W}_{hh}$: Hidden-to-hidden recurrent weight matrix.
    *   $\tanh$: Centers activations to $[-1, 1]$ to scale signals over temporal steps.

## Parameter Sharing & Output Projections

*   **Weight Sharing:** The parameters ($\mathbf{W}_{xh}, \mathbf{W}_{hh}, \mathbf{b}_h$) are shared across all steps $t$. This allows the model to process variable length sequences and find patterns regardless of their position.
*   **Output Prediction:** Hidden states are projected to classification predictions:
    $$\hat{\mathbf{y}}_t = \operatorname{softmax}(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)$$
*   **Padding & Masking:** Shorter sequences are padded with zeros to match batch sizing, and masking blocks updates on pad positions.
