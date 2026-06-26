# Ascendrite Interview Prep: Adaptive Optimizers

## Q1: Why does AdaGrad suffer from premature learning rate decay, and how does RMSprop resolve this mathematically?

### Standard Answer
AdaGrad adapts the learning rate of each parameter by dividing the gradient by the square root of the sum of all historical squared gradients:
$$s_t = s_{t-1} + g_t^2$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{s_t} + \epsilon} g_t$$
Because $g_t^2 \ge 0$, the term $s_t$ is monotonically non-decreasing ($s_t \ge s_{t-1}$). In long training loops, the sum of squared gradients grows extremely large. Consequently, the effective learning rate denominator $\sqrt{s_t} + \epsilon$ approaches infinity, scaling down the parameter updates to near-zero. The model stalls and ceases to learn long before it reaches a local minimum.

RMSprop resolves this by replacing the monotonic sum with an exponentially decaying running average:
$$s_t = \beta s_{t-1} + (1 - \beta) g_t^2$$
where $\beta \in [0, 1)$ is the decay parameter (usually $0.999$). 

Expanding this recursively reveals that the value of $s_t$ is bounded. If we assume the gradient magnitude is bounded by a constant $M$ (i.e., $|g_k| \le M$):
$$s_t = (1 - \beta) \sum_{k=0}^{t-1} \beta^k g_{t-k}^2 \le M^2 (1 - \beta) \sum_{k=0}^{t-1} \beta^k < M^2$$
Because $s_t$ is bounded above by $M^2$, the denominator $\sqrt{s_t} + \epsilon$ remains stable and does not blow up. The memory is limited to a local temporal window of width approximately $\frac{1}{1-\beta}$ steps, preventing premature learning rate decay.

---

## Q2: Derive the bias correction factors for the first moment estimate $\mathbf{m}_t$ in the Adam optimizer.

### Standard Answer
In Adam, the first moment estimate is computed recursively starting from $\mathbf{m}_0 = \mathbf{0}$:
$$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t$$

Expanding this recurrence relation back to step $t=1$:
$$\mathbf{m}_t = (1 - \beta_1) \mathbf{g}_t + \beta_1 \mathbf{m}_{t-1}$$
$$\mathbf{m}_t = (1 - \beta_1) \mathbf{g}_t + \beta_1 \left( (1 - \beta_1) \mathbf{g}_{t-1} + \beta_1 \mathbf{m}_{t-2} \right)$$
$$\mathbf{m}_t = (1 - \beta_1) \sum_{i=1}^t \beta_1^{t-i} \mathbf{g}_i$$

Now, we take the expectation of both sides to assess the estimator's bias. We want to relate the expectation of the estimator, $E[\mathbf{m}_t]$, to the true expectation of the gradient $E[\mathbf{g}_i]$. Under the assumption that the true gradient expectation has stabilized to a constant vector $E[\mathbf{g}]$:
$$E[\mathbf{m}_t] = E\left[ (1 - \beta_1) \sum_{i=1}^t \beta_1^{t-i} \mathbf{g}_i \right]$$
$$E[\mathbf{m}_t] = (1 - \beta_1) \sum_{i=1}^t \beta_1^{t-i} E[\mathbf{g}_i]$$
$$E[\mathbf{m}_t] = E[\mathbf{g}] (1 - \beta_1) \sum_{j=0}^{t-1} \beta_1^j$$

The summation $\sum_{j=0}^{t-1} \beta_1^j$ is a finite geometric series. Applying the geometric sum formula:
$$\sum_{j=0}^{t-1} \beta_1^j = \frac{1 - \beta_1^t}{1 - \beta_1}$$

Substituting this back into the expectation equation:
$$E[\mathbf{m}_t] = E[\mathbf{g}] (1 - \beta_1) \left( \frac{1 - \beta_1^t}{1 - \beta_1} \right) = E[\mathbf{g}] (1 - \beta_1^t)$$

To obtain an unbiased estimator $\hat{\mathbf{m}}_t$ where $E[\hat{\mathbf{m}}_t] = E[\mathbf{g}]$, we must divide by the scaling factor:
$$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}$$

In the early steps of training (small $t$), $1 - \beta_1^t$ is significantly less than 1 (for instance, if $\beta_1 = 0.9$ and $t=1$, the factor is $0.1$), amplifying updates to compensate for the zero-initialization bias. As $t \to \infty$, the term $\beta_1^t \to 0$, and the bias correction factor converges to 1.

---

## Q3: Provide a rigorous explanation of why L2 regularization diverges from decoupled weight decay (AdamW) in adaptive optimizers.

### Standard Answer
L2 regularization adds a penalty to the loss function: $\mathcal{L}_{\text{reg}} = \mathcal{L} + \frac{\lambda}{2} \|\mathbf{\theta}\|_2^2$, which alters the gradients input to the optimizer:
$$\mathbf{g}_t^{\text{reg}} = \mathbf{g}_t + \lambda \mathbf{\theta}_t$$

In adaptive optimizers (like Adam), this modified gradient is used to track the first and second moment estimates. Let's trace how the L2 penalty is processed in the update step (ignoring first-moment momentum and bias corrections for simplicity):
$$\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) (\mathbf{g}_t + \lambda \mathbf{\theta}_t)^2$$
$$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{\sqrt{\mathbf{v}_t} + \epsilon} \odot (\mathbf{g}_t + \lambda \mathbf{\theta}_t)$$

This update splits into a parameter update step and a regularization step:
$$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{\sqrt{\mathbf{v}_t} + \epsilon} \odot \mathbf{g}_t - \frac{\eta \lambda}{\sqrt{\mathbf{v}_t} + \epsilon} \odot \mathbf{\theta}_t$$

Notice the regularization term $- \frac{\eta \lambda}{\sqrt{\mathbf{v}_t} + \epsilon} \odot \mathbf{\theta}_t$:
1.  **Gradient Scale Dependence:** The decay rate is divided by the historical gradient variance $\sqrt{\mathbf{v}_t}$. A parameter that has historically received massive gradients (large $v_{t,i}$) will have its weight decay factor scaled down. Consequently, active parameters receive *less* decay.
2.  **Premature Decay of Sparse Weights:** A parameter that rarely receives gradients (small $v_{t,i}$) will have its weight decay term scaled up by the small denominator, causing its weights to decay to zero much faster.

AdamW solves this by decoupling the weight decay step from the gradient updates, subtracting the decay term directly:
$$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \eta \lambda \mathbf{\theta}_t - \frac{\eta}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \odot \hat{\mathbf{m}}_t$$
This ensures that all parameters decay at a rate strictly proportional to their value, preserving uniform regularization across all layers.
