# Ascendrite Interview Prep: Long Short-Term Memory (LSTM)

## Q1: How do LSTMs mathematically solve the vanishing gradient problem? Trace the gradient path of the cell state.

### Standard Answer
In a standard RNN, the gradient of the hidden state at step $t$ with respect to the state at step $k$ is a product of Jacobian matrices:
$$\frac{\partial \mathbf{h}_t}{\partial \mathbf{h}_k} = \prod_{i=k+1}^t \operatorname{diag}(1 - \tanh^2(\mathbf{z}_i)) \mathbf{W}_{hh}^{\top}$$
Because this requires multiplying the weight matrix $\mathbf{W}_{hh}^{\top}$ repeatedly at each step, the gradient norm scales exponentially with sequence length, leading to vanishing or exploding gradients.

In an LSTM, the long-term memory is carried by the cell state $\mathbf{c}_t$. Its update equation is:
$$\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t$$

During backpropagation, let's compute the derivative of the cell state at step $t$ with respect to the cell state at step $t-1$:
$$\frac{\partial \mathbf{c}_t}{\partial \mathbf{c}_{t-1}} = \operatorname{diag}(\mathbf{f}_t) + \mathbf{c}_{t-1} \odot \frac{\partial \mathbf{f}_t}{\partial \mathbf{c}_{t-1}} + \tilde{\mathbf{c}}_t \odot \frac{\partial \mathbf{i}_t}{\partial \mathbf{c}_{t-1}} + \mathbf{i}_t \odot \frac{\partial \tilde{\mathbf{c}}_t}{\partial \mathbf{c}_{t-1}}$$

This Jacobian has an additive structure. The dominant term is the diagonal matrix of the forget gate activations:
$$\frac{\partial \mathbf{c}_t}{\partial \mathbf{c}_{t-1}} \approx \operatorname{diag}(\mathbf{f}_t)$$

If the network learns to keep the forget gate open (i.e. $\mathbf{f}_t \approx 1.0$), the gradient simplifies to:
$$\frac{\partial \mathbf{c}_t}{\partial \mathbf{c}_{t-1}} \approx I$$

Consequently, the gradient can propagate backward through time over hundreds of steps without decaying or exploding. The error signal flows directly through the additive cell state highway.

---

## Q2: Explain the purpose of each of the four gates/components inside an LSTM cell. Why must we use Sigmoid for gates and Tanh for state updates?

### Standard Answer
An LSTM cell contains three gates and one candidate memory update vector:
1.  **Forget Gate ($\mathbf{f}_t$):** Decides what fraction of the previous cell memory $\mathbf{c}_{t-1}$ to keep.
2.  **Input Gate ($\mathbf{i}_t$):** Decides which elements of the new candidate update $\tilde{\mathbf{c}}_t$ to write to the cell state.
3.  **Candidate State ($\tilde{\mathbf{c}}_t$):** Computes new feature values from the input $\mathbf{x}_t$ and previous hidden state $\mathbf{h}_{t-1}$ to update the cell memory.
4.  **Output Gate ($\mathbf{o}_t$):** Filters what elements of the updated cell state $\mathbf{c}_t$ are exposed in the output hidden state $\mathbf{h}_t$.

**Activation Function Constraints:**
*   **Sigmoid ($\sigma$) for Gates:** The output range of the sigmoid function is strictly $[0, 1]$. This is necessary because gates act as binary probability masks. A value of $0.0$ represents a closed gate (discard information), and $1.0$ represents an open gate (keep all information).
*   **Tanh for State Updates:** The output range of tanh is $[-1, 1]$. This is necessary because updating the cell state requires both additive and subtractive changes. Using a sigmoid (which is strictly positive) would mean the cell state could only increase, leading to numerical saturation. Using tanh allows features to increase or decrease, and centers updates to stabilize scaling.

---

## Q3: What is the 'Forget Gate Bias Initialization' trick, and why is it crucial at the start of training?

### Standard Answer
At the start of training, model weights and biases are initialized near zero.
Under this default initialization, the pre-activation input to the forget gate is near zero:
$$\mathbf{f}_t = \sigma(\mathbf{W}_{xf}\mathbf{x}_t + \mathbf{W}_{hf}\mathbf{h}_{t-1} + \mathbf{b}_f) \approx \sigma(\mathbf{0}) = 0.5$$

A forget gate activation of $0.5$ means that at each time step, half of the cell state information is discarded. Over a sequence of length 10, the gradient scales as $(0.5)^{10} \approx 0.00097$. This causes gradients to vanish immediately at the start of training, preventing the network from learning long-term dependencies.

To resolve this, we initialize the forget gate bias vector $\mathbf{b}_f$ to a high constant value like $1.0$ or $2.0$.
This forces the initial forget gate activations to be:
$$\mathbf{f}_t \approx \sigma(1.0) \approx 0.73 \quad \text{or} \quad \sigma(2.0) \approx 0.88$$
By keeping the forget gate open at the start of training, we ensure that gradients can propagate backward through time, allowing the model to learn long-range context.
