# Ascendrite Revision Layer: Linear & Regularized Regression

## 1. OLS Closed-Form Solution

Minimizes the sum of squared residuals:
$$\mathcal{L}(\mathbf{w}) = \frac{1}{2} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2$$

Setting the gradient to zero yields the **normal equations**:
$$\mathbf{X}^{\top}\mathbf{X}\mathbf{w} = \mathbf{X}^{\top}\mathbf{y}$$

Closed-form solution:
$$\mathbf{w}_{\text{OLS}} = (\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top}\mathbf{y}$$
*   **Condition:** Requires $\mathbf{X}^{\top}\mathbf{X}$ to be non-singular (full column rank).

---

## 2. Ridge (L2) vs. LASSO (L1)

### Ridge Regression
Adds a quadratic penalty:
$$\mathcal{L}_{\text{Ridge}}(\mathbf{w}) = \frac{1}{2} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \frac{\lambda}{2} \|\mathbf{w}\|_2^2$$

Closed-form solution:
$$\mathbf{w}_{\text{Ridge}} = (\mathbf{X}^{\top}\mathbf{X} + \lambda\mathbf{I})^{-1}\mathbf{X}^{\top}\mathbf{y}$$
*   Guarantees invertibility by shifting eigenvalues of $\mathbf{X}^{\top}\mathbf{X}$ upward.

### LASSO Regression
Adds an absolute sum penalty:
$$\mathcal{L}_{\text{LASSO}}(\mathbf{w}) = \frac{1}{2} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda \|\mathbf{w}\|_1$$
*   No closed-form solution. Must be solved using coordinate descent. Encourages weight sparsity (coefficients set to exactly zero).

---

## 3. Bayesian MAP Equivalence

MAP parameter estimation is equivalent to regularized regression:
*   **Gaussian Prior:** $\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \tau^2\mathbf{I}) \iff$ Ridge Regression, where $\lambda = \frac{\sigma^2}{\tau^2}$.
*   **Laplace Prior:** $w_j \sim \text{Laplace}(0, b) \iff$ LASSO Regression, where $\lambda = \frac{\sigma^2}{b}$.
