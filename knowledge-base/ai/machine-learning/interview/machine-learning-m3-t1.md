# Ascendrite Interview Prep: Linear & Regularized Regression

## Q1: Derive the closed-form solution of Ordinary Least Squares (OLS) regression using matrix calculus.

### Standard Answer
We start with the OLS loss function:
$$\mathcal{L}(\mathbf{w}) = \frac{1}{2} (\mathbf{y} - \mathbf{X}\mathbf{w})^{\top}(\mathbf{y} - \\mathbf{X}\mathbf{w})$$
Expanding this expression:
$$\mathcal{L}(\mathbf{w}) = \frac{1}{2} \left( \mathbf{y}^{\top}\mathbf{y} - 2\mathbf{w}^{\top}\mathbf{X}^{\top}\mathbf{y} + \mathbf{w}^{\top}\mathbf{X}^{\top}\mathbf{X}\mathbf{w} \right)$$
Now we take the gradient with respect to $\mathbf{w}$ and set it to zero:
$$\nabla_{\mathbf{w}} \mathcal{L}(\mathbf{w}) = -\mathbf{X}^{\top}\mathbf{y} + \mathbf{X}^{\top}\mathbf{X}\mathbf{w} = \mathbf{0}$$
$$\mathbf{X}^{\top}\mathbf{X}\mathbf{w} = \mathbf{X}^{\top}\mathbf{y}$$
Assuming $\mathbf{X}$ has full column rank, $\mathbf{X}^{\top}\mathbf{X}$ is invertible, yielding:
$$\mathbf{w}_{\text{OLS}} = (\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top}\mathbf{y}$$

---

## Q2: Why does Ridge regression guarantee a solution even when the features are perfectly collinear?

### Standard Answer
When features are collinear, the columns of $\mathbf{X}$ are linearly dependent. This makes the matrix $\mathbf{X}^{\top}\mathbf{X}$ singular (determinant is zero, minimum eigenvalue is zero), which prevents inversion.

Ridge regression modifies the objective by adding $\lambda \|\mathbf{w}\|_2^2$, resulting in the closed-form weight:
$$\mathbf{w}_{\text{Ridge}} = (\mathbf{X}^{\top}\mathbf{X} + \lambda\mathbf{I})^{-1}\mathbf{X}^{\top}\mathbf{y}$$
The regularized matrix $\mathbf{A} = \mathbf{X}^{\top}\mathbf{X} + \lambda\mathbf{I}$ shifts all eigenvalues of $\mathbf{X}^{\top}\mathbf{X}$ upward by $\lambda$. Since eigenvalues of $\mathbf{X}^{\top}\mathbf{X}$ are non-negative, the eigenvalues of $\mathbf{A}$ are strictly greater than or equal to $\lambda > 0$, guaranteeing that $\mathbf{A}$ is positive definite and invertible.

---

## Q3: How do you explain the connection between L1 regularization and a Laplace prior?

### Standard Answer
Under the Bayesian framework, the posterior distribution of weights given the data is proportional to the likelihood multiplied by the prior:
$$P(\mathbf{w} \mid \mathcal{D}) \propto P(\mathcal{D} \mid \mathbf{w}) P(\mathbf{w})$$
Taking the logarithm:
$$\log P(\mathbf{w} \mid \mathcal{D}) \propto \log P(\mathcal{D} \mid \mathbf{w}) + \log P(\mathbf{w})$$
If we assume Gaussian noise, the log-likelihood is proportional to the negative sum of squared residuals: $-\frac{1}{2\sigma^2} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2$.

If we assume the weights are independent and follow a zero-mean Laplace distribution with scale parameter $b$:
$$P(w_j) = \frac{1}{2b} \exp\left(-\frac{|w_j|}{b}\right)$$
The log-prior becomes:
$$\log P(\mathbf{w}) = -d\log(2b) - \frac{1}{b} \|\mathbf{w}\|_1$$
Substituting this back and maximizing the posterior (MAP) is equivalent to minimizing:
$$\mathcal{L}(\mathbf{w}) = \frac{1}{2} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \frac{\sigma^2}{b} \|\mathbf{w}\|_1$$
This is exactly the formulation of LASSO regression, where $\lambda = \frac{\sigma^2}{b}$.
