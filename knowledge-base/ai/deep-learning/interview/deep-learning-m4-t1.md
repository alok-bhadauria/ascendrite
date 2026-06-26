# Ascendrite Interview Prep: Sequential Data & RNN Foundations

## Q1: Why are feedforward neural networks (MLPs) poorly suited for sequential data like text or speech?

### Standard Answer
Standard Feedforward Networks (MLPs) have three main limitations when processing sequential data:
1.  **Fixed-size Input Layer:** An MLP's input layer has a fixed number of neurons. This means they cannot accept sequences of varying lengths (e.g. sentences of 5 words versus 50 words) without truncating or padding them, which is computationally inefficient.
2.  **Lack of Spatial-Temporal Invariance:** If we flatten a sequence to fit it into an MLP, the network must learn the same feature independently at every position. For example, if a key phrase shifts from the beginning to the end of a sentence, the MLP fails to generalize the pattern because it treats each coordinate index separately.
3.  **No Persistence of State:** MLPs have no memory mechanism. They process each input vector in isolation. In sequential tasks, context is critical (e.g. interpreting the word 'bank' requires reading preceding words like 'river' or 'money').

---

## Q2: Write down the state transition equation of an Elman RNN cell. Explain the dimension matching for all matrices and vectors.

### Standard Answer
The state transition equation of an Elman RNN cell is:
$$\mathbf{h}_t = \tanh(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)$$

**Dimension Matching:**
Let:
*   $d$ be the input feature dimension (e.g., word embedding size).
*   $h$ be the hidden state representation dimension (channels).
*   $N$ be the batch size.

The dimensions of the variables are:
*   **Input vector ($\mathbf{x}_t$):** Shape is $(d, N)$ (or $(d, 1)$ for a single sequence).
*   **Previous hidden state ($\mathbf{h}_{t-1}$):** Shape is $(h, N)$.
*   **Input weight matrix ($\mathbf{W}_{xh}$):** Shape is $(h, d)$.
*   **Recurrent weight matrix ($\mathbf{W}_{hh}$):** Shape is $(h, h)$.
*   **Bias vector ($\mathbf{b}_h$):** Shape is $(h, 1)$ (which is broadcasted across the batch dimension $N$).
*   **Output hidden state ($\mathbf{h}_t$):** Shape is $(h, N)$.

**Dimension Check inside activation:**
*   $\mathbf{W}_{xh} \mathbf{x}_t \to (h, d) \times (d, N) = (h, N)$
*   $\mathbf{W}_{hh} \mathbf{h}_{t-1} \to (h, h) \times (h, N) = (h, N)$
*   Summing these vectors yields shape $(h, N)$, which matches the shape of the bias and output $\mathbf{h}_t$.

---

## Q3: What is the principle of temporal parameter sharing in RNNs? What are its benefits?

### Standard Answer
**Temporal Parameter Sharing** means that the same set of weight matrices ($\mathbf{W}_{xh}$, $\mathbf{W}_{hh}$) and bias vectors ($\mathbf{b}_h$) are used at every time step $t = 1, 2, \dots, T$ of the sequence.

**Benefits:**
1.  **Variable Sequence Lengths:** Because the transition parameters are identical, we can run the recurrence loop for any number of steps $T$ without altering the model definition.
2.  **Generalization across Positions:** Sharing parameters allows the model to learn features that generalize across different temporal positions. If the model learns that a word like 'not' reverses sentiment at step 2, it can apply the same rule at step 10.
3.  **Parameter Efficiency:** If we used separate weights for each time step $t$, the parameter count would grow linearly with the sequence length, leading to overfitting and scaling issues.
