# Ascendrite Interview Prep: Gated Recurrent Units (GRU)

## Q1: Compare LSTMs and GRUs in terms of parameter counts, structural math, and training characteristics.

### Standard Answer
**1. Parameter Footprint and Structural Complexity:**
*   **LSTMs** use four sets of parameter matrices corresponding to: Forget Gate ($\mathbf{f}_t$), Input Gate ($\mathbf{i}_t$), Candidate Cell State ($\tilde{\mathbf{c}}_t$), and Output Gate ($\mathbf{o}_t$).
*   **GRUs** combine the input and forget gates into a single Update Gate ($\mathbf{z}_t$), eliminate the output gate in favor of a Reset Gate ($\mathbf{r}_t$), and collapse the cell state and hidden state into a single Hidden State ($\mathbf{h}_t$). They only use three sets of parameter matrices (reset gate, update gate, candidate state).
*   **Parameter Ratio:** For the same hidden dimension $h$ and input dimension $d$, a GRU uses approximately 25% fewer parameters than an LSTM.

**2. Training Characteristics:**
*   Because GRUs have a smaller parameter footprint, they require less GPU memory, can process larger batches, and train faster. They are also less prone to overfitting on smaller target datasets.
*   LSTMs, having a separate cell state and hidden state, have higher expressive capacity and can model more complex, long-range sequential relationships given sufficient training data.

---

## Q2: Write down the GRU state update equations. Highlight where the Reset Gate is applied and explain the student trap regarding it.

### Standard Answer
At each step $t$, given input $\mathbf{x}_t$ and previous state $\mathbf{h}_{t-1}$:
1.  **Reset Gate:** $\mathbf{r}_t = \sigma(\mathbf{W}_{xr} \mathbf{x}_t + \mathbf{W}_{hr} \mathbf{h}_{t-1} + \mathbf{b}_r)$
2.  **Update Gate:** $\mathbf{z}_t = \sigma(\mathbf{W}_{xz} \mathbf{x}_t + \mathbf{W}_{hz} \mathbf{h}_{t-1} + \mathbf{b}_z)$
3.  **Candidate Hidden State:** $\tilde{\mathbf{h}}_t = \tanh(\mathbf{W}_{xh} \mathbf{x}_t + \mathbf{r}_t \odot (\mathbf{W}_{hh} \mathbf{h}_{t-1}) + \mathbf{b}_h)$
4.  **Hidden State Update:** $\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$

**Reset Gate Application and Student Trap:**
*   The Reset Gate $\mathbf{r}_t$ is applied to the **previous hidden state** $\mathbf{h}_{t-1}$ *before* it is multiplied by the recurrent weight matrix $\mathbf{W}_{hh}$.
*   **The Trap:** Students often apply $\mathbf{r}_t$ to the entire pre-activation sum: $\mathbf{r}_t \odot (\mathbf{W}_{xh} \mathbf{x}_t + \mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{b}_h)$, or to the input $\mathbf{x}_t$. This is incorrect. The reset gate modulates only the history $\mathbf{h}_{t-1}$ to decide how much past context is mixed into the new candidate.

---

## Q3: How does the GRU hidden state update equation act as a linear interpolation? What is its impact on gradient flow?

### Standard Answer
The GRU hidden state update is:
$$\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$$

This equation is a **linear interpolation** (or weighted average) between the previous hidden state $\mathbf{h}_{t-1}$ and the new candidate hidden state $\tilde{\mathbf{h}}_t$, modulated by the update gate vector $\mathbf{z}_t$.

*   **Copying Memory:** If the update gate $\mathbf{z}_t$ is close to $\mathbf{0}$, then $\mathbf{h}_t \approx \mathbf{h}_{t-1}$. The cell copies its previous hidden state forward without updating, allowing information to persist over many steps.
*   **Overwriting Memory:** If $\mathbf{z}_t$ is close to $\mathbf{1}$, then $\mathbf{h}_t \approx \tilde{\mathbf{h}}_t$. The old memory is overwritten by the new candidate.

**Impact on Gradient Flow:**
During backpropagation, the derivative of the state at step $t$ with respect to step $t-1$ contains the term $(1 - \mathbf{z}_t)$. If the network learns to keep the update gate closed ($\mathbf{z}_t \approx \mathbf{0}$), the gradient propagates backward through time with a scale of approximately $1.0$, preventing it from vanishing or exploding.
