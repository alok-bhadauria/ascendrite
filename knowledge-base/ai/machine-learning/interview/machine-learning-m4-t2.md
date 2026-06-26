# Ascendrite Interview Prep: Advanced Cross-Validation Protocols

## Q1: Why does standard K-Fold cross-validation introduce 'selection bias' when used for both hyperparameter optimization and model evaluation? How does Nested Cross-Validation resolve this?

### Standard Answer
*   **The Cause of Selection Bias:**
    If we use a single K-Fold loop, we partition the data into training and validation folds, evaluate multiple hyperparameter configurations (e.g. grid search), and select the configuration $\theta^*$ that yields the highest average validation score. This validation score is a maximum over multiple trials. Because we used the validation set to direct our search, the selected model is tuned specifically to perform well on those validation folds. Reporting this validation score as the estimated generalization error introduces **selection bias**, resulting in an overoptimistic assessment of the model's performance on unseen data.
*   **The Nested Cross-Validation Solution:**
    Nested Cross-Validation solves this by using two concentric loops:
    1.  **Outer Loop:** Splits the global dataset into $K_{\text{outer}}$ test and training folds. The outer test folds are held out strictly for evaluating the final model's performance.
    2.  **Inner Loop:** For each outer split, an inner $K_{\text{inner}}$-fold cross-validation is executed strictly on the outer training set to find the optimal hyperparameters $\theta^*$.
    3.  **Evaluation:** The model is retrained on the entire outer training set using $\theta^*$ and evaluated on the completely unseen outer test fold. By nesting the hyperparameter selection *inside* the outer loop, the test data is kept completely isolated from the tuning process, providing an unbiased generalization estimate.

---

## Q2: You are training a medical image classifier where the dataset contains multiple images from the same patient. If you perform a standard random train-test split, what mathematical and generalization failures will occur, and how does Stratified Group K-Fold resolve them?

### Standard Answer
*   **Failure Modes of Random Splitting:**
    If patient images are split randomly, images from the same patient will appear in both the training set and the validation set. This violates the independent and identically distributed (i.e.d.) assumption because images belonging to a single patient share high correlation (e.g., identical anatomical structures, camera lighting, sensor noise).
    1.  **Data Leakage:** The model will memorize patient-specific identifiers rather than general disease features.
    2.  **Overoptimistic Metrics:** The validation accuracy will be artificially high because the model is tested on known patient anatomies.
    3.  **Generalization Collapse:** In production, when evaluated on completely new patients, accuracy will collapse because the model never learned to generalize across patients.
*   **Resolution via Stratified Group K-Fold:**
    1.  **Group Isolation:** It ensures that all images belonging to a specific patient group (grouped by a patient ID key) are assigned strictly to the same fold. The model is validated only on patients it has never seen during training, simulating real-world clinical deployment.
    2.  **Class Balance (Stratification):** It distributes the patient groups among folds such that the ratio of disease classes in each validation fold matches the global class distribution as closely as possible, preventing class-balance drift between splits.

---

## Q3: Explain why random K-Fold splits are unacceptable for time-series forecasting, and contrast the expanding window versus sliding window walk-forward validation protocols.

### Standard Answer
*   **Failure of Random K-Fold:**
    Time-series observations are sequentially ordered and autocorrelated. Random K-Fold splits break this temporal structure, allowing training on future data (e.g. time $t+1$) to predict past data (e.g. time $t$). This introduces **future-lookahead target leakage** and violates causality, as models in production cannot query future values. Additionally, highly correlated adjacent values (at $t-1$ and $t+1$) leak the target at $t$ during validation, producing artificially low validation error.
*   **Expanding Window Walk-Forward Validation:**
    *   **Mechanics:** At split $k$, we train on all historical data $\{t_1, \dots, t_k\}$ and validate on the next future segment $\{t_{k+1}, \dots, t_{k+h}\}$. At step $k+1$, the training window expands to include $\{t_1, \dots, t_{k+h}\}$ and validates on the subsequent segment.
    *   **Use Case:** Best when the underlying data-generating process is stationary and the model benefits from a larger history to compute stable parameters.
*   **Sliding Window Walk-Forward Validation:**
    *   **Mechanics:** The training window is constrained to a fixed size $W$. At split $k$, we train on $\{t_{k-W}, \dots, t_k\}$ and validate on $\{t_{k+1}, \dots, t_{k+h}\}$.
    *   **Use Case:** Preferred for non-stationary environments (e.g., financial markets or user behavior trends) where older data is outdated. Restricting training to a sliding window forces the model to ignore stale data and adapt quickly to distribution shifts.
