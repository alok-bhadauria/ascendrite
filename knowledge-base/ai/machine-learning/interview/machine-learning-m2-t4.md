# Ascendrite Interview Prep: Exploratory Data Analysis & Target Leakage

## Q1: How do you mathematically define the Variance Inflation Factor (VIF), and why does a high VIF indicate collinearity?

### Standard Answer
The Variance Inflation Factor (VIF) for feature $X_j$ is defined as:
$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
where $R_j^2$ is the coefficient of determination from an auxiliary linear regression of $X_j$ against the remaining features $\mathbf{X}_{-j}$.

If $X_j$ is highly collinear with the other features, the auxiliary regression will achieve a near-perfect fit, meaning $R_j^2 \to 1$. As $R_j^2$ approaches 1, the denominator $(1 - R_j^2) \to 0$, causing the $\text{VIF}_j$ to grow toward infinity. This directly reflects that the variance of coefficient $\beta_j$ is inflated, making the estimate unstable.

---

## Q2: Your model achieves 99.9% AUC on validation sets but drops to 50% AUC in production. Walk me through your diagnostics steps.

### Standard Answer
This is a classic symptom of **target leakage**. I would diagnose it using the following steps:
1.  **Check Feature Importance:** I will extract the model's feature importances. If one or two features dominate (e.g., holding $98\%$ of the split weight), I will flag them for closer inspection.
2.  **Conduct a Timeline Audit:** I will review the time-delta between when the features are computed and when the target variable becomes known in the database. Any feature incorporating information from after the prediction event is leaked.
3.  **Inspect Split Mechanics:** I will verify if scaling or imputations were performed globally before cross-validation splitting, which leaks validation fold statistics into the training loop.
4.  **Baseline Testing:** I will re-train the model without the suspected features and verify if the validation AUC drops to a realistic level.

---

## Q3: Why is standard K-Fold cross-validation unsuitable for sequential or time-series datasets?

### Standard Answer
Standard K-Fold cross-validation splits datasets randomly. For sequential data, this allows future data points to appear in the training fold while past data points are used for validation. This violates the temporal boundary of the production environment, introducing timeline leakage and making validation metrics artificially optimistic. We must use time-series splits (`TimeSeriesSplit`), where the validation fold always follows the training fold.
