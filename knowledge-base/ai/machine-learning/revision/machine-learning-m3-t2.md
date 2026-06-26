# Ascendrite Revision Layer: Logistic Regression & Log-Loss

## 1. Sigmoid Function and Derivative

Squashes linear outputs to probability space $(0, 1)$:
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Derivative expressed in terms of the function value:
$$\sigma'(z) = \sigma(z)(1 - \sigma(z))$$
*   **Gradient Saturation:** Max value is $0.25$ (at $z = 0$). As $|z| \to \infty$, the derivative vanishes to zero, causing learning to stall.

---

## 2. Loss Function and Gradient Derivation

### Binary Cross-Entropy (Log-Loss)
Derived from joint Bernoulli likelihood of target labels $y_i \in \{0, 1\}$:
$$\mathcal{L}(\mathbf{w}) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \log p_i + (1 - y_i) \log(1 - p_i) \right]$$
where $p_i = \sigma(\mathbf{x}_i^{\\top}\mathbf{w})$.

### Gradient Vector
$$\nabla_{\mathbf{w}} \mathcal{L}(\mathbf{w}) = \frac{1}{N} \mathbf{X}^{\top}(\mathbf{p} - \mathbf{y})$$
where $\mathbf{p} = \sigma(\mathbf{X}\mathbf{w})$.

---

## 3. Second-Order Optimization: IRLS

Newton-Raphson weight updates scale the gradient by the inverse of the Hessian matrix:
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \mathbf{H}^{-1} \nabla_{\mathbf{w}} \mathcal{L}(\mathbf{w})$$

*   **Hessian Matrix:** $\mathbf{H} = \mathbf{X}^{\top}\mathbf{S}\mathbf{X}$, where $\mathbf{S}$ is a diagonal matrix containing variances: $S_{ii} = p_i(1 - p_i)$. Because $S_{ii} > 0$, the Hessian is positive definite, proving the log-loss is strictly convex.
*   **IRLS (Iteratively Reweighted Least Squares) Formulation:**
    $$\mathbf{w}_{t+1} = (\mathbf{X}^{\top}\mathbf{S}_t\mathbf{X})^{-1} \mathbf{X}^{\top}\mathbf{S}_t\mathbf{z}_t$$
    where $\mathbf{z}_t = \mathbf{X}\mathbf{w}_t + \mathbf{S}_t^{-1}(\mathbf{y} - \mathbf{p}_t)$ is the adjusted response vector.
*   **Complexity:** Requires $\mathcal{O}(d^3)$ operations per iteration to invert the $d \times d$ Hessian matrix.
