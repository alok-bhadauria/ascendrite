# Ascendrite Interview Prep: Bagging & Random Forests

## Q1: Prove that the variance of an ensemble of $B$ bagged estimators is bounded by $\rho \sigma^2$, where $\sigma^2$ is the individual model variance and $\rho$ is the pairwise correlation.

### Standard Answer
Let $X_1, \dots, X_B$ be identically distributed random variables representing predictions of individual models, each with variance $\text{Var}(X_i) = \sigma^2$ and positive pairwise correlation $\text{Corr}(X_i, X_j) = \rho > 0$ for $i \neq j$. By definition of correlation, the covariance is $\text{Cov}(X_i, X_j) = \rho \sigma^2$.

The ensemble prediction is the sample average $Y = \frac{1}{B} \sum_{i=1}^B X_i$. We compute the variance of $Y$:
$$\text{Var}(Y) = \text{Var}\left( \frac{1}{B} \\sum_{i=1}^B X_i \right) = \frac{1}{B^2} \text{Var}\left( \sum_{i=1}^B X_i \right)$$

Using the algebraic expansion of the variance of a sum of random variables:
$$\text{Var}(Y) = \frac{1}{B^2} \left[ \sum_{i=1}^B \text{Var}(X_i) + \sum_{i=1}^B \sum_{j \neq i}^B \text{Cov}(X_i, X_j) \right]$$

Since there are $B$ variance terms and $B(B-1)$ covariance terms:
$$\text{Var}(Y) = \frac{1}{B^2} \left[ B \sigma^2 + B(B - 1) \rho \sigma^2 \right]$$
$$\text{Var}(Y) = \frac{\sigma^2}{B} + \frac{B - 1}{B} \rho \sigma^2 = \frac{\sigma^2}{B} + \rho \sigma^2 - \frac{\rho \sigma^2}{B}$$
$$\text{Var}(Y) = \rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2$$

Taking the limit as the number of models $B \to \infty$:
$$\lim_{B \to \infty} \text{Var}(Y) = \rho \sigma^2$$

This mathematically proves that the variance of a bagged ensemble cannot be reduced to zero. It is lower-bounded by $\rho \sigma^2$, which depends strictly on how correlated the individual trees are.

---

## Q2: Show mathematically why approximately $36.8\%$ of training observations are excluded from a single bootstrap sample of size $N$ as $N \to \infty$. Describe how this result is utilized in Out-of-Bag (OOB) error estimation.

### Standard Answer
*   **Mathematical Proof:**
    Let a dataset contain $N$ unique observations. In bootstrap sampling, we draw $N$ times with replacement.
    1.  The probability of selecting a specific observation $\mathbf{x}_i$ in a single draw is $\frac{1}{N}$.
    2.  The probability of *not* selecting $\mathbf{x}_i$ in a single draw is $1 - \frac{1}{N}$.
    3.  Because each draw is independent and we make $N$ total draws, the probability that $\mathbf{x}_i$ is never selected is:
        $$p = \left( 1 - \frac{1}{N} \right)^N$$
    4.  To find the asymptotic behavior for large datasets, we evaluate the limit as $N \to \infty$:
        $$\lim_{N \to \infty} \left( 1 - \frac{1}{N} \right)^N$$
        Using the standard calculus limit identity $\lim_{x \to \infty} (1 - \frac{a}{x})^x = e^{-a}$ with $a=1$:
        $$\lim_{N \to \infty} \left( 1 - \frac{1}{N} \right)^N = e^{-1} \approx 0.36787$$
    Thus, for large $N$, any given bootstrap sample will omit approximately $36.8\%$ of the original observations.

*   **Utilization in OOB Estimation:**
    1.  During training, each tree $h_b$ is trained on a bootstrap sample $\mathcal{D}_b$, leaving a known set of OOB observations.
    2.  For each observation $\mathbf{x}_i$ in the original dataset, we identify the subset of trees $\{h_b\}$ that did not include $\mathbf{x}_i$ in their training split.
    3.  We pass $\mathbf{x}_i$ through this subset of trees and aggregate their predictions.
    4.  Comparing these OOB predictions with the true target labels $y_i$ yields the OOB error. Because the trees used to predict $\mathbf{x}_i$ did not train on it, the OOB error serves as an unbiased estimate of the model's true generalization performance, bypassing the need for a separate validation split.

---

## Q3: Explain how Random Forests improves upon standard bagging. Discuss the bias-variance trade-off associated with the `max_features` ($m$) hyperparameter.

### Standard Answer
*   **The Limitation of Standard Bagging:**
    In standard bagging, the trees are highly correlated ($\rho$ is high). If a few features in the dataset are highly predictive, almost all decision trees will select those same features for their top splits. This structural similarity keeps $\rho$ high, which limits the ensemble's ability to reduce variance.
*   **The Random Forests Solution:**
    Random Forests introduces **feature subspace sampling**. When growing each tree, at each split node, the algorithm only searches a randomly selected subset of $m$ features (typically $m = \sqrt{d}$) to execute the split. This forces trees to split on different features, generating structurally diverse trees and reducing the correlation $\rho$ between predictions.
*   **Bias-Variance Trade-off of `max_features` ($m$):**
    *   **Decreasing $m$ (Lower $m$):**
        *   **Variance:** Decreases. Trees become more structurally diverse, which reduces the correlation $\rho$ between trees and drives down the ensemble variance limit $\rho \sigma^2$.
        *   **Bias:** Increases. Because the split selection is constrained to a small subset, trees may miss the optimal split feature, making individual trees weaker (higher individual variance $\sigma^2$ and higher bias).
    *   **Increasing $m$ (Higher $m$):**
        *   **Bias:** Decreases. Individual trees have access to all/most features and can construct optimal splits, reducing individual bias.
        *   **Variance:** Increases. Trees select the same dominant features, increasing tree correlation $\rho$ and raising the ensemble variance limit.
