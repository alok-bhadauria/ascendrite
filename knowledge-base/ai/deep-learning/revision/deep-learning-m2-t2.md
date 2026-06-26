# Ascendrite Revision Layer: Adaptive Optimizers

## 1. AdaGrad vs. RMSprop Update Dynamics

Adaptive optimizers scale the step size of each parameter individually:
*   **AdaGrad:** Scales by the running sum of squared gradients:
    $$\mathbf{s}_t = \mathbf{s}_{t-1} + \mathbf{g}_t \odot \mathbf{g}_t$$
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{\sqrt{\mathbf{s}_t} + \epsilon} \odot \mathbf{g}_t$$
    *   **Limitation:** $\mathbf{s}_t$ grows monotonically, causing the effective learning rate to shrink to zero, stopping learning prematurely.
*   **RMSprop:** Scales by the exponentially decaying running average of squared gradients (decay factor $\beta$):
    $$\mathbf{s}_t = \beta \mathbf{s}_{t-1} + (1 - \beta) \mathbf{g}_t \odot \mathbf{g}_t$$
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{\sqrt{\mathbf{s}_t} + \epsilon} \odot \mathbf{g}_t$$
    *   **Advantage:** Prevents premature termination of learning by restricting memory to a local temporal window of past gradients.

---

## 2. The Adam Optimizer

Adam tracks the first moment $\mathbf{m}_t$ (momentum) and the second moment $\mathbf{v}_t$ (scaling variance):
$$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t$$
$$\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t \odot \mathbf{g}_t$$

### Bias Correction
Because $\mathbf{m}_0 = \mathbf{0}$ and $\mathbf{v}_0 = \mathbf{0}$, the moment estimates are biased toward zero in the early steps. We correct the bias using the factors $(1 - \beta_1^t)$ and $(1 - \beta_2^t)$:
$$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t} \quad \text{and} \quad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}$$

### Parameter Update Step
$$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \odot \hat{\mathbf{m}}_t$$

---

## 3. L2 Regularization vs. Decoupled Weight Decay (AdamW)

*   **L2 Regularization:** Adds $\lambda \mathbf{\theta}_t$ directly to the gradient $\mathbf{g}_t$ before calculating moment estimates:
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \odot (\hat{\mathbf{m}}_t + \lambda \mathbf{\theta}_t)$$
    *   **Issue:** Parameters with historically large gradients receive *less* regularization because the term is divided by $\sqrt{\hat{\mathbf{v}}_t}$. Parameters with small gradients decay too fast.
*   **Decoupled Weight Decay (AdamW):** Applies the weight decay step directly to the parameters, bypassing the gradient moment updates entirely:
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \eta \lambda \mathbf{\theta}_t - \frac{\eta}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \odot \hat{\mathbf{m}}_t$$
    This restores uniform weight decay across all parameters, which is vital for stabilizing Transformer architectures.
