# Ascendrite Revision Layer: Model Evaluation & Class Imbalance Mitigation

## 1. Evaluation Curves & Skewed Distributions

### ROC-AUC vs. PR-AUC
*   **ROC Curve:** Plots True Positive Rate (Recall) vs. False Positive Rate.
    $$\text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \quad \text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$$
    *   *Limitation:* In highly imbalanced datasets ($N_{\text{neg}} \gg N_{\text{pos}}$), the massive number of True Negatives keeps the FPR artificially low, making ROC-AUC misleadingly optimistic.
*   **PR Curve:** Plots Precision vs. Recall (TPR).
    $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
    *   *Strength:* Focuses strictly on positive prediction performance, independent of TN. PR-AUC is highly sensitive to False Positives.

### $F_\beta$ Score
Generalizes F1-score to control the relative weight of Precision and Recall:
$$F_\beta = (1 + \beta^2) \frac{\text{Precision} \times \text{Recall}}{\beta^2 \text{Precision} + \text{Recall}}$$
*   $\beta = 1$: $F_1$ score (harmonic mean).
*   $\beta > 1$: Prioritizes Recall (e.g. medical diagnosis).
*   $\beta < 1$: Prioritizes Precision (e.g. spam detection).

---

## 2. Averaging Schemas & SMOTE Interpolation

### Multi-Class Averaging
*   **Macro Average:** Unweighted arithmetic mean of class-wise metrics. Treats all classes equally, highlighting minority class drops.
*   **Micro Average:** Computes metric globally across pooled TPs, FPs, and FNs. Dominated by majority class.
*   **Weighted Average:** Multiplies each class metric by its support ratio $\frac{N_k}{N}$.

### SMOTE Algorithm
Generates synthetic minority samples by linear interpolation:
$$\mathbf{x}_{\text{new}} = \mathbf{x}_i + \lambda (\mathbf{x}_{nn} - \mathbf{x}_i)$$
where $\mathbf{x}_{nn}$ is a randomly selected $k$-nearest neighbor of minority sample $\mathbf{x}_i$, and $\lambda \sim \text{Uniform}(0, 1)$.
*   *Warning:* Apply SMOTE *strictly after* train-test splitting to prevent target leakage.

---

## 3. Cost-Sensitive Loss Functions

### Class-Weighted Loss
Adjusts the cross-entropy loss by scaling contributions based on class frequency:
$$\mathcal{L}_{\text{CW}} = -\sum_{i=1}^N w_{y_i} \log(p_{t,i}), \quad \text{where } w_k = \frac{N}{K \cdot N_k}$$

### Focal Loss
Modulates standard cross-entropy with a focusing factor $(1 - p_t)^\gamma$ to down-weight easy examples:
$$\text{FL}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$
where $p_t = p$ for $y=1$ and $1-p$ for $y=0$.
*   **$\gamma$ (Focusing Parameter):** $\gamma \ge 0$. Larger $\gamma \implies$ less gradient weight on easy-to-classify samples ($p_t \to 1$), forcing the optimizer to target hard, misclassified boundary instances.
