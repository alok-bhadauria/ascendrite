# Ascendrite Revision Card: Sequence-to-Sequence (Seq2Seq)

## Encoder-Decoder Framework

*   **Encoder:** Processes the input sequence to output a fixed-size context vector $\mathbf{v}$ (typically the final hidden state $\mathbf{h}_{T_x}$).
*   **Decoder:** Takes $\mathbf{v}$ as its initial state and autoregressively generates the output sequence.
*   **Bottleneck:** Forcing a variable-length sequence into a single fixed-size vector degrades performance on long sequences.

## Teacher Forcing Strategy

*   **Training:** Feeds the ground-truth target token $y_{t-1}$ directly as input to the decoder at step $t$ instead of feeding the decoder's own prediction $\hat{y}_{t-1}$. This accelerates training convergence.
*   **Exposure Bias Trap:** Mismatch between training (perfect inputs) and inference (autoregressive predictions). Early prediction errors during inference can cause cascading failures because the model drifts into unfamiliar state regions.

## Recurrent Attention Mechanisms

*   **Luong (Multiplicative) Attention:** Computes alignment scores between the current decoder state $\mathbf{s}_t$ and encoder states $\mathbf{h}_i^{\text{enc}}$:
    $$s_{\text{Luong}}(\mathbf{s}_t, \mathbf{h}_i^{\text{enc}}) = \mathbf{s}_t^{\top} \mathbf{W}_a \mathbf{h}_i^{\text{enc}}$$
    *   *Pros:* Fast and memory-efficient (can be written as a single matrix multiplication).
*   **Bahdanau (Additive) Attention:** Computes alignment scores using the previous decoder state $\mathbf{s}_{t-1}$:
    $$s_{\text{Bahdanau}}(\mathbf{s}_{t-1}, \mathbf{h}_i^{\text{enc}}) = \mathbf{v}_a^{\top} \tanh(\mathbf{W}_a \mathbf{s}_{t-1} + \mathbf{U}_a \mathbf{h}_i^{\text{enc}})$$
    *   *Cons:* Computationally slower due to the addition and activation steps.

## Context Aggregation & Attentional Projections

1.  **Softmax Weights:** Normalize alignment scores:
    $$\alpha_{t, i} = \frac{\exp(s_t, \mathbf{h}_i^{\text{enc}})}{\sum_j \exp(s_t, \mathbf{h}_j^{\text{enc}})}$$
2.  **Context Vector:** Weighted sum of encoder hidden states:
    $$\mathbf{c}_t = \sum_i \alpha_{t, i} \mathbf{h}_i^{\text{enc}}$$
3.  **Attentional State:** Concatenate $\mathbf{c}_t$ and $\mathbf{s}_t$ and project:
    $$\tilde{\mathbf{s}}_t = \tanh(\mathbf{W}_c [\mathbf{c}_t ; \mathbf{s}_t] + \mathbf{b}_c)$$
