# Ascendrite Revision Layer: Regularization Techniques

## 1. L1 vs. L2 Weight Regularization

Regularization restricts the capacity of parameter matrices to prevent overfitting:
*   **L2 Regularization (Weight Decay):**
    $$\mathcal{L}_{\text{L2}}(\mathbf{\theta}) = \mathcal{L}_0(\mathbf{\theta}) + \frac{\lambda}{2} \lVert\mathbf{\theta}\rVert_2^2$$
    $$\mathbf{\theta}_{t+1} = (1 - \eta \lambda) \mathbf{\theta}_t - \eta \nabla_{\mathbf{\theta}} \mathcal{L}_0(\mathbf{\theta}_t)$$
    *   **Effect:** Subtracts a portion of the parameter weight proportional to its size on each step. Scales down large weights uniformly while keeping them non-zero.
*   **L1 Regularization (Lasso):**
    $$\mathcal{L}_{\text{L1}}(\mathbf{\theta}) = \mathcal{L}_0(\mathbf{\theta}) + \lambda \lVert\mathbf{\theta}\rVert_1$$
    $$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t - \eta \lambda \operatorname{sgn}(\mathbf{\theta}_t) - \eta \nabla_{\mathbf{\theta}} \mathcal{L}_0(\mathbf{\theta}_t)$$
    *   **Effect:** Subtracts a constant rate $\eta \lambda$ from the parameter weight on each step, regardless of weight scale. Forces small weights to exactly zero, yielding sparse parameter matrices.

---

## 2. Inverted Dropout Mechanics

Inverted Dropout scales active weights during training to keep the test pass clean of modifications.
*   **Forward Pass (Training):**
    Generate binary Bernoulli mask $\mathbf{r}^{(l)}$ with keep probability $1-p$:
    $$\mathbf{a}^{(l)}_{\text{train}} = \frac{\mathbf{r}^{(l)}}{1-p} \odot f(\mathbf{z}^{(l)})$$
*   **Forward Pass (Inference):**
    No changes or scaling applied:
    $$\mathbf{a}^{(l)}_{\text{test}} = f(\mathbf{z}^{(l)})$$
*   **Backward Pass (Training):**
    Error delta is masked and scaled matching the forward pass:
    $$\boldsymbol{\delta}^{(l)} = \left( \mathbf{W}^{(l+1)\top} \boldsymbol{\delta}^{(l+1)} \right) \odot \frac{\mathbf{r}^{(l)}}{1-p} \odot f^{\prime}(\mathbf{z}^{(l)})$$

---

## 3. Early Stopping

Monitors generalization capacity during training to stop optimization before overfitting occurs.
*   **Checking Metric:** Validation loss $\mathcal{L}_{\text{val}}(t)$ evaluated per epoch.
*   **Parameters:**
    *   `min_delta`: minimum decrease to qualify as an improvement.
    *   `patience`: number of epochs to wait for improvement before stopping.
*   **Update Steps:**
    *   If $\mathcal{L}_{\text{val}}(t) < \mathcal{L}_{\text{best}} - \text{min\_delta}$:
        *   Save best parameters: $\mathbf{\theta}_{\text{best}} = \mathbf{\theta}_t$.
        *   Reset patience counter: $c = 0$.
    *   Else:
        *   Increment counter: $c = c + 1$.
        *   If $c \ge \text{patience}$: terminate training and restore parameters to $\mathbf{\theta}_{\text{best}}$.
