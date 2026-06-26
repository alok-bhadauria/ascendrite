# Ascendrite Interview Prep: Anomaly Detection & Time Series

## Q1: Explain how Isolation Forests isolate anomalies. Detail the mathematical normalization term $c(N)$ and the anomaly score formula.

### Standard Answer
*   **Isolation Mechanism:**
    Unlike distance-based or density-based models that profile normal points, Isolation Forests isolate anomalies directly. The feature space is recursively partitioned using random axis-aligned splits. Because anomalies are sparse and reside far from dense clusters in coordinate space, they require significantly fewer random splits to be isolated in a leaf node, resulting in short tree path lengths.
*   **Average BST Path Length Normalization ($c(N)$):**
    As dataset size $N$ increases, tree depth and path length naturally grow. To compare path lengths across varying sample sizes, we normalize the observed path length $h(\mathbf{x})$ using the average path length of an unsuccessful search in a Binary Search Tree (BST) built on $N$ points:
    $$c(N) = 2 \ln(N - 1) + 0.5772156649 - \frac{2(N - 1)}{N}$$
    where $0.5772156649$ is Euler's constant. This term represents the expected path length of a balanced random partition structure.
*   **Anomaly Score Formula:**
    The anomaly score $s(\mathbf{x}, N)$ is defined as:
    $$s(\mathbf{x}, N) = 2^{-\frac{\mathbb{E}[h(\mathbf{x})]}{c(N)}}$$
    where $\mathbb{E}[h(\mathbf{x})]$ is the average path length of sample $\mathbf{x}$ across all trees in the forest.
    *   **$s \to 1$ (Anomaly):** If the average path length is very small ($\mathbb{E}[h(\mathbf{x})] \to 0$), the exponent approaches 0, yielding a score close to 1.
    *   **$s \to 0.5$ (Normal):** If the average path length matches the BST average ($\mathbb{E}[h(\mathbf{x})] \to c(N)$), the exponent is $-1$, yielding a score of $0.5$.
    *   **$s \to 0$ (Typical):** If the path length is long ($\mathbb{E}[h(\mathbf{x})] \to N$), the score approaches 0.

---

## Q2: Detail the One-Class SVM optimization objective and constraints. How does the parameter $\nu$ function in controlling the decision boundary?

### Standard Answer
The One-Class SVM maps the input data into a high-dimensional feature space using a mapping function $\Phi(\mathbf{x})$ and finds the hyperplane that separates the normal data points from the coordinate origin with maximum margin.

The primal optimization objective is formulated as:
$$\min_{\mathbf{w}, \boldsymbol{\xi}, \rho} \frac{1}{2} \|\mathbf{w}\|_2^2 + \frac{1}{\nu N} \sum_{i=1}^N \xi_i - \rho$$
$$\text{subject to} \quad \mathbf{w}^{\top} \Phi(\mathbf{x}_i) \ge \rho - \xi_i, \quad \xi_i \ge 0, \quad \forall i$$
where $\mathbf{w}$ is the weight vector normal to the hyperplane, $\rho$ is the margin offset from the origin, and $\xi_i$ are slack variables for margin violations.

**The Role of $\nu$ (Nu-property):**
The regularization parameter $\nu \in (0, 1]$ controls the trade-off between the margin size and the penalization of points falling on the wrong side of the boundary. It has two critical mathematical properties:
1.  **Upper Bound on Outliers:** $\nu$ represents the maximum fraction of training samples allowed to be classified as outliers (anomalies, where $\xi_i > 0$).
2.  **Lower Bound on Support Vectors:** $\nu$ represents the minimum fraction of training samples that must serve as support vectors (lying on or inside the margin boundary).

Tuning $\nu$ allows engineers to directly align the decision boundary with a target false positive rate or expected contamination ratio in the training set.

---

## Q3: Define weak stationarity in time-series data. Formulate the Augmented Dickey-Fuller (ADF) test, and explain why stationarity is a prerequisite for fitting ARIMA models.

### Standard Answer
*   **Weak Stationarity:**
    A time series $Y_t$ is weakly stationary if its joint probability distribution is invariant under time shifts. This requires:
    1.  Constant Mean: $\mathbb{E}[Y_t] = \mu$ for all $t$.
    2.  Constant Variance: $\text{Var}(Y_t) = \sigma^2$ for all $t$.
    3.  Constant Autocovariance: $\text{Cov}(Y_t, Y_{t-k}) = \gamma_k$ for all $t$, depending only on the lag $k$, not the time index $t$.

*   **The ADF Test Formulation:**
    The ADF test checks for the presence of a unit root (non-stationarity) by fitting the regression model:
    $$\Delta Y_t = \alpha + \beta t + \gamma Y_{t-1} + \sum_{i=1}^p \delta_i \Delta Y_{t-i} + \epsilon_t$$
    where $\Delta Y_t = Y_t - Y_{t-1}$ is the first difference.
    *   **Null Hypothesis $H_0$:** $\gamma = 0$ (a unit root exists, indicating the series is non-stationary).
    *   **Alternative Hypothesis $H_1$:** $\gamma < 0$ (no unit root exists, indicating the series is stationary).

*   **Prerequisite for ARIMA:**
    ARIMA models model linear temporal relationships assuming that the statistical properties (mean and covariance structure) are stable.
    1.  **Mean Stability:** If a series has a trend (non-stationary mean), the parameters of the Autoregressive $\text{AR}(p)$ model will be biased, attempting to fit a moving baseline, which causes predictions to drift.
    2.  **Variance Stability:** If variance grows over time, the Moving Average $\text{MA}(q)$ parameters will fail to model residuals properly, leading to unstable error terms.
    Stationarity (achieved via the differencing step $d$ in ARIMA) ensures the data oscillates around a constant mean with constant variance, allowing AR and MA parameters to model stable linear relationships.
