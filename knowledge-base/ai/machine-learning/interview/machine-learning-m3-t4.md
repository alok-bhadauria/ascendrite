# Ascendrite Interview Prep: Support Vector Machines (SVM)

## Q1: How does the regularization parameter $C$ in a soft-margin SVM affect the margin, and what is its impact on the bias-variance trade-off?

### Standard Answer
The regularization parameter $C > 0$ controls the trade-off between maximizing the geometric margin and minimizing individual margin violations (slack variables $\xi_i$):

$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2} \|\mathbf{w}\|_2^2 + C \sum_{i=1}^N \xi_i$$

1.  **High $C$ (Low Bias, High Variance):**
    *   The optimizer is heavily penalized for any margin violations ($\xi_i > 0$).
    *   This forces the margin to narrow to accommodate data points close to the decision boundary, striving for zero training error.
    *   The model becomes sensitive to noise and individual outliers, leading to high variance (overfitting).
2.  **Low $C$ (High Bias, Low Variance):**
    *   The optimizer tolerates margin violations to achieve a larger margin width (smaller $\|\mathbf{w}\|_2$).
    *   The decision boundary is determined by a broader consensus of points, reducing the influence of individual outliers.
    *   The model gains stability (low variance) at the expense of higher training bias (potential underfitting).

---

## Q2: Explain the Karush-Kuhn-Tucker (KKT) complementary slackness conditions for the soft-margin SVM, and describe how they identify support vectors.

### Standard Answer
For soft-margin SVM, the KKT complementary slackness conditions associate the inequality constraints with their Lagrange multipliers at the optimal solution:

$$\lambda_i \left( y_i(\mathbf{w}^{\top}\mathbf{x}_i + b) - 1 + \xi_i \right) = 0$$

$$\mu_i \xi_i = 0 \implies (C - \lambda_i)\xi_i = 0$$

where $\lambda_i$ are the multipliers for the margin constraints, $\mu_i$ are the multipliers for the slack non-negativity constraints, and $\lambda_i + \mu_i = C$.

These conditions group training observations into three distinct categories:
1.  **Non-Support Vectors ($\lambda_i = 0$):**
    *   Since $\lambda_i = 0$, we have $\mu_i = C$. The condition $\mu_i\xi_i = 0$ forces $\xi_i = 0$.
    *   The margin constraint is strictly satisfied: $y_i(\mathbf{w}^{\top}\mathbf{x}_i + b) > 1$.
    *   These points lie outside the margin and do not affect the decision boundary.
2.  **Margin Support Vectors ($0 < \lambda_i < C$):**
    *   Since $0 < \lambda_i < C$, the second condition $(C - \lambda_i)\xi_i = 0$ forces $\xi_i = 0$.
    *   The first condition forces $y_i(\mathbf{w}^{\top}\mathbf{x}_i + b) - 1 = 0$, meaning these points lie exactly on the margin boundaries.
    *   These points define the orientation of the hyperplane.
3.  **Non-Margin Support Vectors ($\lambda_i = C$):**
    *   Since $\lambda_i = C$, we have $\mu_i = 0$, allowing $\xi_i > 0$.
    *   These points violate the margin. If $\xi_i \le 1$, they are correctly classified but lie within the margin. If $\xi_i > 1$, they are misclassified.

---

## Q3: Prove that the Radial Basis Function (RBF) kernel projects input data into an infinite-dimensional feature space.

### Standard Answer
The Radial Basis Function (RBF) kernel is defined as:

$$K(\mathbf{x}_i, \mathbf{x}_j) = \exp\left(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|_2^2\right)$$

Let $\gamma = 1$ and consider the 1D case ($x_i, x_j \in \mathbb{R}$). Expanding the squared distance in the exponent yields:

$$K(x_i, x_j) = e^{-(x_i - x_j)^2} = e^{-x_i^2 - x_j^2 + 2x_i x_j} = e^{-x_i^2} e^{-x_j^2} e^{2x_i x_j}$$

We apply the Taylor series expansion for the exponential function, $e^z = \sum_{k=0}^{\infty} \frac{z^k}{k!}$, to the term $e^{2x_i x_j}$:

$$e^{2x_i x_j} = \sum_{k=0}^{\infty} \frac{(2x_i x_j)^k}{k!} = \sum_{k=0}^{\infty} \frac{2^k x_i^k x_j^k}{k!}$$

Substituting this back into the kernel formulation:

$$K(x_i, x_j) = e^{-x_i^2} e^{-x_j^2} \sum_{k=0}^{\infty} \frac{2^k x_i^k x_j^k}{k!} = \sum_{k=0}^{\infty} \left( e^{-x_i^2} \sqrt{\frac{2^k}{k!}} x_i^k \right) \left( e^{-x_j^2} \sqrt{\frac{2^k}{k!}} x_j^k \right)$$

This expression can be rewritten as the dot product of two infinite-dimensional vectors $\Phi(x_i)^{\top}\Phi(x_j)$, where the mapping function $\Phi(x)$ is defined as:

$$\Phi(x) = e^{-x^2} \left[ 1, \sqrt{\frac{2}{1!}}x, \sqrt{\frac{2^2}{2!}}x^2, \dots, \sqrt{\frac{2^k}{k!}}x^k, \dots \right]^{\top}$$

Because the feature vector $\Phi(x)$ has an infinite number of components, the RBF kernel implicitly maps the input space to an infinite-dimensional Hilbert space.
