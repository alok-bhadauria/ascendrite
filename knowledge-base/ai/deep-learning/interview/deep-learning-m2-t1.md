# Ascendrite Interview Prep: Optimization Algorithms

## Q1: Explain how classical momentum mathematically dampens gradient oscillations in directions of high curvature while accelerating learning along low-curvature valley floors.

### Standard Answer
Consider a loss surface resembling a narrow ravine, where the gradient along the high-curvature direction (say, axis $y$) is large and alternates signs, while the gradient along the low-curvature direction (axis $x$) is small but consistently points towards the local minimum.

The momentum velocity update is:
$$v_{t+1} = \beta v_t + \eta g_t$$
where $g_t$ is the current gradient. 

If we expand this relation recursively:
$$v_t = \eta \sum_{k=0}^{t-1} \beta^k g_{t-1-k}$$
For the high-curvature axis $y$, the gradients $g^{(y)}$ alternate signs. Summing these alternating signs causes them to cancel each other out over successive steps, keeping $v^{(y)}$ small. This effectively dampens the wild oscillations across the ravine walls.

For the low-curvature axis $x$, the gradients $g^{(x)}$ consistently carry the same sign. The term $\sum_{k=0}^{t-1} \beta^k$ acts as a geometric series. As $t \to \infty$, it converges to the limit:
$$\frac{1}{1 - \beta}$$
Thus, if $\beta = 0.9$, the velocity in the consistent direction accelerates to a maximum speed of $\frac{1}{1 - 0.9} = 10$ times the speed of standard SGD, accelerating progress along the valley floor.

---

## Q2: What is the mathematical and conceptual difference between classical momentum and Nesterov Accelerated Gradient (NAG)?

### Standard Answer
The difference lies in where the gradient of the loss function is evaluated.

*   **Classical Momentum** evaluates the gradient at the current parameter position $\mathbf{\theta}_t$:
    $$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \eta \nabla_{\mathbf{\theta}} \mathcal{L}(\mathbf{\theta}_t)$$
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \mathbf{v}_{t+1}$$
*   **Nesterov Momentum** evaluates the gradient at a look-ahead parameter position $\mathbf{\theta}_t - \beta \mathbf{v}_t$, which represents a prediction of where the parameters will be after the momentum decay step:
    $$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \eta \nabla_{\mathbf{\theta}} \mathcal{L}(\mathbf{\theta}_t - \beta \mathbf{v}_t)$$
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \mathbf{v}_{t+1}$$

**The Damping Mechanism:**
If the current momentum velocity is carrying the parameters up a steep hill ahead, the look-ahead point $\mathbf{\theta}_t - \beta \mathbf{v}_t$ lies further up the slope than the current point $\mathbf{\theta}_t$. The gradient calculated at this look-ahead point will be much larger in the opposite direction than the gradient at the current position. Consequently, Nesterov momentum injects an early corrective force that dampens the parameters' velocity before they actually overshoot the local minimum, providing superior stability and faster convergence.

---

## Q3: What are the theoretical and practical justifications for employing a learning rate warm-up schedule at the beginning of deep network training?

### Standard Answer
At the start of training, the model parameters $\mathbf{\theta}$ are randomly initialized, meaning the network's predictions are highly inaccurate and the initial losses are massive.

1.  **Preventing early parameter saturation and divergence:** If we immediately use a large learning rate $\eta_{\max}$, the massive initial gradients will trigger extremely large parameter updates. In layers with sigmoid or tanh activations, this pushes pre-activations into saturated regions (where derivatives are close to zero), leading to dead neurons. In self-attention layers, it can cause numerical overflows.
2.  **Stabilizing adaptive optimizers:** Adaptive optimizers like Adam keep a running average of historical squared gradients. In the first few steps, these running averages are highly unstable due to low sample sizes. A warm-up phase limits update steps while these variance estimates stabilize.

Practically, a linear warm-up starts $\eta$ at 0 and increases it linearly to $\eta_{\max}$ over the first few thousand iterations (or epochs). This allows the network parameters to settle into a stable configuration before high-speed convergence schedules are applied.
