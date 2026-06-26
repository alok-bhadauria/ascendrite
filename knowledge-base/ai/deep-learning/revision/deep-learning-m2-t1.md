# Ascendrite Revision Layer: Optimization Algorithms

## 1. Gradient Descent Paradigms

Given learning rate $\eta$, batch size $B$, and dataset size $N$:
*   **Batch Gradient Descent ($B = N$):**
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{N} \sum_{i=1}^N \nabla_{\mathbf{\theta}} \mathcal{L}_i(\mathbf{\theta}_t)$$
    Zero variance, computationally expensive, guarantees convergence to local/global minimum.
*   **Stochastic Gradient Descent ($B = 1$):**
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \eta \nabla_{\mathbf{\theta}} \mathcal{L}_i(\mathbf{\theta}_t)$$
    High variance, escapes saddle points, requires learning rate decay to stabilize.
*   **Mini-Batch Gradient Descent ($1 < B < N$):**
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \frac{\eta}{B} \sum_{i \in \mathcal{B}} \nabla_{\mathbf{\theta}} \mathcal{L}_i(\mathbf{\theta}_t)$$
    Balances variance and speed, exploits GPU vectorization.

---

## 2. Momentum Acceleration

Dampens oscillations in high-curvature directions and accelerates down flat valleys.
*   **Classical Momentum:**
    $$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \eta \nabla_{\mathbf{\theta}} \mathcal{L}(\mathbf{\theta}_t)$$
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \mathbf{v}_{t+1}$$
    where $\beta \in [0, 1)$ is the velocity decay factor (typically $0.9$).
*   **Nesterov Accelerated Gradient (NAG):**
    Calculates gradient at a projected look-ahead position:
    $$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \eta \nabla_{\mathbf{\theta}} \mathcal{L}(\mathbf{\theta}_t - \beta \mathbf{v}_t)$$
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \mathbf{v}_{t+1}$$

---

## 3. Learning Rate Schedulers

Decays $\eta$ over epochs to refine parameters near local minima:
*   **Step Decay:** Decays $\eta$ by factor $\gamma$ every $k$ steps:
    $$\eta_t = \eta_0 \cdot \gamma^{\lfloor t/k \rfloor}$$
*   **Exponential Decay:** Smooth exponential reduction:
    $$\eta_t = \eta_0 \cdot e^{-kt}$$
*   **Cosine Annealing:** Smooth wave decay matching cosine profile:
    $$\eta_t = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min})\left(1 + \cos\left(\frac{T_{\text{cur}}}{T_{\text{max}}}\pi\right)\right)$$
*   **Linear Warm-up:** Linearly increases $\eta$ over first $W$ steps to stabilize early training:
    $$\eta_t = \frac{t}{W} \eta_{\max} \quad \text{for } t \le W$$
