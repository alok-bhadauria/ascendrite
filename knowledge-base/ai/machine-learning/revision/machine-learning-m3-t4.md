# Ascendrite Revision Layer: Support Vector Machines (SVM)

## 1. Primal Optimization and Margins

### Hard-Margin SVM (Linearly Separable)
Maximize the margin width $\frac{2}{\|\mathbf{w}\|_2}$:
$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|_2^2 \quad \text{subject to} \quad y_i(\mathbf{w}^{\top}\mathbf{x}_i + b) \ge 1, \quad \forall i$$

### Soft-Margin SVM (Non-Separable / Robust)
Introduce slack variables $\xi_i \ge 0$:
$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2} \|\mathbf{w}\|_2^2 + C \sum_{i=1}^N \xi_i$$
$$\text{subject to} \quad y_i(\mathbf{w}^{\top}\mathbf{x}_i + b) \ge 1 - \xi_i \quad \text{and} \quad \xi_i \ge 0, \quad \forall i$$
*   **$C$ role:** Regularization parameter. Large $C \implies$ small margin violations (narrow margin, high variance). Small $C \implies$ permits margin violations (wide margin, high bias).

---

## 2. Dual Formulation and KKT Conditions

### Dual Optimization Problem
Maximize parameters in the dual space under box constraints:
$$\max_{\boldsymbol{\lambda}} \sum_{i=1}^N \lambda_i - \frac{1}{2} \sum_{i=1}^N \sum_{j=1}^N \lambda_i \lambda_j y_i y_j \mathbf{x}_i^{\top}\mathbf{x}_j$$
$$\text{subject to} \quad \sum_{i=1}^N \lambda_i y_i = 0 \quad \text{and} \quad 0 \le \lambda_i \le C, \quad \forall i$$
Weights derived via dual variables: $\mathbf{w} = \sum_{i=1}^N \lambda_i y_i \mathbf{x}_i$.

### KKT Complementary Slackness
Optimal solutions must satisfy:
$$\lambda_i \left( y_i(\mathbf{w}^{\top}\mathbf{x}_i + b) - 1 + \xi_i \right) = 0$$
$$(C - \lambda_i)\xi_i = 0$$
*   $\lambda_i = 0$: Point outside margin, correctly classified.
*   $0 < \lambda_i < C$: Margin support vector ($\xi_i = 0$, lies exactly on margin boundary).
*   $\lambda_i = C$: Violates margin ($\xi_i > 0$, lies inside margin or misclassified).

---

## 3. Kernel Trick and Mercer's Theorem

### Mercer's Theorem
A symmetric function $K(\mathbf{x}_i, \mathbf{x}_j)$ is a valid kernel if and only if its Gram matrix $\mathbf{K}$ is positive semi-definite. It implicitly computes the inner product $\Phi(\mathbf{x}_i)^{\top}\Phi(\mathbf{x}_j)$ in a projected Hilbert space.

### Radial Basis Function (RBF) Kernel
$$K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|_2^2)$$
*   **$\gamma$ role:** Controls width of kernel. Large $\gamma \implies$ small radius of influence (leads to overfitting). Small $\gamma \implies$ large radius of influence (leads to underfitting).
