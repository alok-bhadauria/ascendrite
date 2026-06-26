# Ascendrite Interview Prep: Model Evaluation & Class Imbalance Mitigation

## Q1: Why can the Receiver Operating Characteristic Area Under the Curve (ROC-AUC) be highly misleading under extreme class imbalance, and why does the Precision-Recall AUC (PR-AUC) provide a more representative evaluation?

### Standard Answer
ROC-AUC evaluates the trade-off between the True Positive Rate (TPR) and the False Positive Rate (FPR):

$$\text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \quad \text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$$

When there is a severe class imbalance where the negative class size $N_{\text{neg}}$ is massive relative to the positive class size $N_{\text{pos}}$:
1.  **FPR Insensitivity:** The denominator for FPR is $\text{FP} + \text{TN} = N_{\text{neg}}$. Because $N_{\text{neg}}$ is exceptionally large, even if the model predicts many False Positives (FPs), the denominator suppresses the FPR fraction, keeping it close to zero.
2.  **Optimism Bias:** As a result, the ROC curve shifts rapidly to the upper-left, yielding an inflated ROC-AUC score (e.g. $0.99$), even when the model makes a massive number of incorrect positive predictions.

PR-AUC evaluates Precision against Recall (TPR):

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

1.  **Sensitivity to False Positives:** Precision focuses exclusively on the positive predictions, meaning $\text{FP}$ appears directly in the denominator alongside $\text{TP}$. True Negatives (TNs) are completely excluded.
2.  **Representative Skew:** Even a moderate increase in False Positives will drastically drop Precision, collapsing the PR-AUC score. Therefore, PR-AUC is far more sensitive to the False Positive rate, making it a reliable performance indicator under high class skew.

---

## Q2: Detail the SMOTE over-sampling algorithm. What is the cause of target leakage when using SMOTE, and what is the correct workflow to prevent it?

### Standard Answer
**Synthetic Minority Over-sampling Technique (SMOTE)** balances dataset classes by generating synthetic minority examples. Given a minority class vector $\mathbf{x}_i \in \mathbb{R}^d$:
1.  Compute the Euclidean distance from $\mathbf{x}_i$ to all other minority samples. Identify its $k$-nearest neighbors.
2.  Randomly select one neighbor $\mathbf{x}_{nn}$.
3.  Generate a synthetic point $\mathbf{x}_{\text{new}}$ along the line segment between them:
    $$\mathbf{x}_{\text{new}} = \mathbf{x}_i + \lambda (\mathbf{x}_{nn} - \mathbf{x}_i)$$
    where $\lambda \sim \text{Uniform}(0, 1)$.

**Target Leakage Cause:**
If SMOTE is applied to the entire dataset *before* partitioning it into train/validation/test splits, synthetic observations in the validation/test splits are derived from nearest neighbors in the training split. This introduces information from the test split directly into the training distribution, leading to:
1.  Severely over-optimistic evaluation metrics during validation.
2.  Poor generalization and model collapse when deployed to unseen production data.

**Correct Workflow:**
1.  Split the raw dataset into training and test folds first.
2.  Compute and apply SMOTE over-sampling *strictly on the training fold*.
3.  Keep the validation and test folds untouched, preserving their natural class distribution.

---

## Q3: Derive the binary Focal Loss objective and explain how the focusing parameter $\gamma$ controls the gradient updates during backpropagation.

### Standard Answer
Focal Loss addresses extreme foreground-background class imbalance by dynamically scaling standard cross-entropy loss based on prediction confidence.

Let $p \in [0, 1]$ be the model's predicted probability for class $1$. We define the correct-class probability $p_t$ as:
$$p_t = \begin{cases} p & \text{if } y = 1 \\ 1 - p & \text{if } y = 0 \end{cases}$$

The standard cross-entropy (CE) loss is:
$$\text{CE}(p_t) = -\log(p_t)$$

Focal Loss introduces a modulating factor $(1 - p_t)^{\gamma}$ and a class-balancing parameter $\alpha_t$:
$$\text{FL}(p_t) = -\alpha_t (1 - p_t)^{\gamma} \log(p_t)$$

where $\gamma \ge 0$ is the focusing parameter.

**Gradient Modulating Behavior:**
Let's analyze the derivative of the loss with respect to the pre-activation logit $z$ (where $p = \sigma(z)$). For $y=1$ (so $p_t = p$):
$$\text{FL}(p) = -\alpha (1 - p)^{\gamma} \log(p)$$

Differentiating with respect to $p$ (using the product rule):
$$\frac{\partial \text{FL}}{\partial p} = -\alpha \left[ -\gamma(1 - p)^{\gamma-1} \log(p) + \frac{(1 - p)^{\gamma}}{p} \right]$$

Since $\frac{\partial p}{\partial z} = p(1 - p)$, the gradient with respect to $z$ is:
$$\frac{\partial \text{FL}}{\partial z} = \frac{\partial \text{FL}}{\partial p} \frac{\partial p}{\partial z} = -\alpha (1-p)^{\gamma+1} \left[ -\frac{\gamma p \log(p)}{1-p} + 1 \right]$$

*   **Easy Examples ($p_t \to 1$):** If the model is confident and correct ($p \to 1$), the factor $(1 - p)^{\gamma+1}$ vanishes rapidly to zero for $\gamma > 0$. The gradient contribution becomes negligible.
*   **Hard Examples ($p_t \to 0$):** If the model is incorrect ($p \to 0$), the factor $(1 - p)^{\gamma+1}$ approaches 1. The gradient updates remain large, forcing the optimizer to focus parameter updates on the hard examples rather than being overwhelmed by the cumulative gradients of easy negative samples.
