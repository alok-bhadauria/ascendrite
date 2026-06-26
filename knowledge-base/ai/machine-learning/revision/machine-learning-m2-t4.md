# Ascendrite Revision Layer: Exploratory Data Analysis & Target Leakage

## 1. Multicollinearity and VIF

*   **Multicollinearity:** Near-perfect linear dependency among multiple features. It destabilizes linear regression weight estimates by making the covariance matrix $(\mathbf{X}^{\top}\mathbf{X})$ nearly singular.
*   **Variance Inflation Factor (VIF):** Measures the inflation of coefficient variance due to collinearity:
    $$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
    where $R_j^2$ is the coefficient of determination from regressing feature $X_j$ against all other features $\mathbf{X}_{-j}$.
*   **Thresholds:**
    *   $\text{VIF}_j > 5$: Moderate collinearity.
    *   $\text{VIF}_j > 10$: Severe collinearity; indicates a redundant feature that should be removed.

---

## 2. Target Leakage Pathways

1.  **Timeline-Based Leakage:** Computing features using future values that are unavailable at prediction time.
2.  **Preprocessing Leakage:** Scaling, imputing, or encoding using statistics computed globally across the entire dataset before splitting.
3.  **Duplicated Record Leakage:** Splitting highly correlated or identical observations (e.g., patient diagnostics from the same visit) across train and test sets.

---

## 3. Prevention Checklist

*   [ ] Use time-based split methods (`TimeSeriesSplit`) for chronological data.
*   [ ] Wrap scaling and imputations in pipeline classes (`Pipeline`) to restrict fitting to the training set.
*   [ ] Remove features with extremely high importance weights (e.g., $>0.95$) that indicate leakage.
