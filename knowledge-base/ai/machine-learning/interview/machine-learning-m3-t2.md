# Ascendrite Interview Prep: Logistic Regression & Log-Loss

## Q1: Why do we use Log-Loss instead of Mean Squared Error (MSE) to train a Logistic Regression model?

### Standard Answer
There are two primary reasons why Log-Loss (Binary Cross-Entropy) is preferred over MSE for classification:
1.  **Optimization Convexity:** Combining the MSE loss function with the non-linear sigmoid activation function yields a non-convex surface containing multiple local minima and plateaus. In contrast, Log-Loss is strictly convex, guaranteeing that optimization methods will locate the unique global minimum.
2.  **Gradient Saturation Mitigation:** If we use MSE, the gradient of the loss with respect to weight $w_j$ is:
    $$\frac{\partial \mathcal{L}_{\text{MSE}}}{\partial w_j} = (p_i - y_i) \cdot p_i(1 - p_i) \cdot x_{i,j}$$
    The term $p_i(1 - p_i)$ is the derivative of the sigmoid function. If the model makes a highly confident but incorrect prediction (e.g. $p_i = 1$ when $y_i = 0$), this term becomes zero. This causes the gradient to vanish, trapping the parameters in a saturated state. Under Log-Loss, this derivative term cancels out:
    $$\frac{\partial \mathcal{L}_{\text{Log-Loss}}}{\partial w_j} = (p_i - y_i) x_{i,j}$$
    The gradient remains proportional to the raw prediction error, ensuring strong parameter updates even when the prediction is highly incorrect.

---

## Q2: Walk me through the derivation of the Hessian matrix for Logistic Regression, and explain how it dictates convexity.

### Standard Answer
We start with the gradient vector of the log-loss:
$$\nabla_{\mathbf{w}} \mathcal{L}(\mathbf{w}) = \mathbf{X}^{\top}(\mathbf{p} - \mathbf{y})$$
To compute the Hessian, we differentiate the gradient with respect to $\mathbf{w}^{\top}$:
$$\mathbf{H} = \frac{\partial^2 \mathcal{L}}{\partial \mathbf{w} \partial \mathbf{w}^{\top}} = \frac{\partial}{\partial \mathbf{w}^{\top}} \left[ \mathbf{X}^{\top}(\mathbf{p} - \mathbf{y}) \right] = \mathbf{X}^{\top} \frac{\partial \mathbf{p}}{\partial \mathbf{w}^{\top}}$$
Using the chain rule, for each element $p_i = \sigma(\mathbf{x}_i^{\top}\mathbf{w})$, the derivative is:
$$\frac{\partial p_i}{\partial \mathbf{w}^{\top}} = p_i(1 - p_i) \mathbf{x}_i^{\top}$$
Stacking these rows yields $\frac{\partial \mathbf{p}}{\partial \mathbf{w}^{\top}} = \mathbf{S}\mathbf{X}$, where $\mathbf{S} = \operatorname{diag}(\mathbf{p}(1 - \mathbf{p}))$. Substituting this back:
$$\mathbf{H} = \mathbf{X}^{\top}\mathbf{S}\mathbf{X}$$
Since $p_i \in (0, 1)$, all diagonal elements of $\mathbf{S}$ are strictly positive. For any non-zero vector $\mathbf{v}$, the quadratic form is:
$$\mathbf{v}^{\top}\mathbf{H}\mathbf{v} = \mathbf{v}^{\top}\mathbf{X}^{\top}\mathbf{S}\mathbf{X}\mathbf{v} = (\mathbf{X}\mathbf{v})^{\top}\mathbf{S}(\mathbf{X}\mathbf{v}) = \sum_{i=1}^N S_{ii} (\mathbf{x}_i^{\top}\mathbf{v})^2 \ge 0$$
Assuming $\mathbf{X}$ has full column rank, this value is strictly positive ($>0$), proving that the Hessian is positive definite, which mathematically guarantees that the log-loss is strictly convex.

---

## Q3: What is the computational complexity of each iteration of the IRLS algorithm, and how does it scale compared to Gradient Descent?

### Standard Answer
At each iteration of IRLS, we must solve a weighted least squares problem requiring the computation and inversion of the Hessian matrix:
$$\mathbf{w}_{t+1} = (\mathbf{X}^{\top}\mathbf{S}_t\mathbf{X})^{-1} \mathbf{X}^{\top}\mathbf{S}_t\mathbf{z}_t$$
*   **Hessian Matrix Multiplication:** Computing $\mathbf{X}^{\top}\mathbf{S}_t\mathbf{X}$ has a time complexity of $\mathcal{O}(N \cdot d^2)$, where $N$ is the sample size and $d$ is the number of features.
*   **Inversion Step:** Inverting the $d \times d$ matrix has a time complexity of $\mathcal{O}(d^3)$.
*   **Comparison:** First-order Gradient Descent only requires computing the gradient vector, which scales as $\mathcal{O}(N \cdot d)$ per step. While IRLS converges in fewer steps (usually under 10 due to quadratic convergence), its $\mathcal{O}(N \cdot d^2 + d^3)$ per-iteration cost makes it scale poorly compared to GD when the feature dimension $d$ is large.
