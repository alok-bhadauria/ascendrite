# Ascendrite Interview Prep: Sequence-to-Sequence (Seq2Seq)

## Q1: What is Teacher Forcing in Seq2Seq models? Explain the trade-offs, specifically defining 'Exposure Bias'.

### Standard Answer
**Teacher Forcing** is a training strategy for sequence generation models (like decoders in Seq2Seq) where the ground-truth target token $y_{t-1}$ is fed as input to the decoder at step $t$ instead of the decoder's own predicted token $\hat{y}_{t-1}$ from the previous step.

**Trade-offs:**
*   **Advantage (Stable Training):** Early in training, the model's predictions are poor. If we feed these incorrect predictions back as inputs, the model's states will drift, and it will struggle to learn valid sequences. Teacher forcing anchors the decoder to the correct trajectory, accelerating convergence.
*   **Disadvantage (Exposure Bias):** This creates a training-inference mismatch. During training, the model is exposed only to ground-truth history. During inference, ground-truth targets are unavailable, so the decoder must run autoregressively (using its own predictions as inputs). If it makes a single incorrect prediction, the error propagates, causing the decoder to drift into regions of parameter space it was never exposed to during training, leading to cascading failures.

---

## Q2: Compare Luong (multiplicative) and Bahdanau (additive) attention mechanisms. Write down their score equations and compare their computational efficiency.

### Standard Answer
The key differences lie in how they calculate alignment scores and which decoder states they use:

**1. Luong (Multiplicative) Attention:**
*   Uses the **current** decoder state $\mathbf{s}_t$ and the encoder states $\mathbf{h}_i^{\text{enc}}$.
*   **Score Equation:**
    $$s_{\text{Luong}}(\mathbf{s}_t, \mathbf{h}_i^{\text{enc}}) = \mathbf{s}_t^{\top} \mathbf{W}_a \mathbf{h}_i^{\text{enc}}$$
*   Where $\mathbf{W}_a$ is a learnable weight matrix.

**2. Bahdanau (Additive) Attention:**
*   Uses the **previous** decoder state $\mathbf{s}_{t-1}$ and the encoder states $\mathbf{h}_i^{\text{enc}}$.
*   **Score Equation:**
    $$s_{\text{Bahdanau}}(\mathbf{s}_{t-1}, \mathbf{h}_i^{\text{enc}}) = \mathbf{v}_a^{\top} \tanh(\mathbf{W}_a \mathbf{s}_{t-1} + \mathbf{U}_a \mathbf{h}_i^{\text{enc}})$$
*   Where $\mathbf{W}_a$ and $\mathbf{U}_a$ are weight matrices, and $\mathbf{v}_a$ is a projection vector.

**3. Computational Efficiency:**
*   **Luong Multiplicative Attention** is highly efficient. The scores for an entire sequence can be computed as a single matrix multiplication: $\mathbf{S}^{\top} \mathbf{W}_a \mathbf{H}$. This leverages optimized hardware operations (BLAS/Tensor Cores).
*   **Bahdanau Additive Attention** requires computing intermediate sums and passing them through a tanh activation. This consumes more memory and is slower because it cannot be fully parallelized into a single matrix product.

---

## Q3: Outline the mathematical steps to calculate the attention context vector $\mathbf{c}_t$ and the attentional hidden state $\tilde{\mathbf{s}}_t$ at step $t$.

### Standard Answer
Given the decoder hidden state $\mathbf{s}_t$ and all encoder hidden states $\mathbf{h}_1^{\text{enc}}, \dots, \mathbf{h}_{T_x}^{\text{enc}}$:

**Step 1: Compute raw alignment scores** (e.g. using Luong multiplicative score):
$$e_{t, i} = \mathbf{s}_t^{\top} \mathbf{W}_a \mathbf{h}_i^{\text{enc}} \quad \text{for each } i = 1 \dots T_x$$

**Step 2: Normalize scores using Softmax** to obtain attention weights:
$$\alpha_{t, i} = \frac{\exp(e_{t, i})}{\sum_{j=1}^{T_x} \exp(e_{t, j})}$$

**Step 3: Compute the Context Vector** $\mathbf{c}_t$ as the weighted sum of encoder hidden states:
$$\mathbf{c}_t = \sum_{i=1}^{T_x} \alpha_{t, i} \mathbf{h}_i^{\text{enc}}$$

**Step 4: Compute the Attentional Hidden State** $\tilde{\mathbf{s}}_t$ by concatenating the context vector and the decoder hidden state, followed by a linear projection and activation:
$$\tilde{\mathbf{s}}_t = \tanh(\mathbf{W}_c [\mathbf{c}_t ; \mathbf{s}_t] + \mathbf{b}_c)$$
This vector $\tilde{\mathbf{s}}_t$ is then used to predict the output token and is passed to the next step.
