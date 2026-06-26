import numpy as np


def compute_f_beta_score(
    y_true: np.ndarray, y_pred: np.ndarray, beta: float = 1.0
) -> float:
    """Computes the F-beta score for binary classification.

    Formula:
        F_beta = (1 + beta^2) * (Precision * Recall) / ((beta^2 * Precision) + Recall)

    Args:
        y_true: Ground truth binary labels vector of shape (n_samples,).
        y_pred: Predicted binary labels vector of shape (n_samples,).
        beta: Weighting parameter. beta > 1 favors recall, beta < 1 favors precision.

    Returns:
        float: Computed F-beta score.
    """
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    if precision == 0.0 and recall == 0.0:
        return 0.0

    numerator = (1.0 + beta**2) * precision * recall
    denominator = (beta**2 * precision) + recall

    return float(numerator / denominator)


def compute_multiclass_f1_averages(
    y_true: np.ndarray, y_pred: np.ndarray
) -> tuple[float, float, float]:
    """Computes the Macro, Micro, and Weighted averages of the F1-score in a multi-class setting.

    Args:
        y_true: Ground truth multi-class labels of shape (n_samples,).
        y_pred: Predicted multi-class labels of shape (n_samples,).

    Returns:
        tuple: (macro_f1, micro_f1, weighted_f1)
            - macro_f1: arithmetic mean of class-wise F1-scores.
            - micro_f1: F1-score computed over global true positives, false positives, false negatives.
            - weighted_f1: average of class-wise F1-scores weighted by class support.
    """
    classes = np.unique(y_true)
    n_classes = len(classes)
    n_samples = len(y_true)

    # Class-wise values
    f1_scores = np.zeros(n_classes)
    class_supports = np.zeros(n_classes)

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for idx, c in enumerate(classes):
        # Counts for this class
        tp = np.sum((y_true == c) & (y_pred == c))
        fp = np.sum((y_true != c) & (y_pred == c))
        fn = np.sum((y_true == c) & (y_pred != c))

        total_tp += tp
        total_fp += fp
        total_fn += fn

        # Class F1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        if precision + recall > 0.0:
            f1_scores[idx] = 2.0 * (precision * recall) / (precision + recall)
        else:
            f1_scores[idx] = 0.0

        class_supports[idx] = np.sum(y_true == c)

    # 1. Macro F1
    macro_f1 = float(np.mean(f1_scores))

    # 2. Micro F1
    global_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    global_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = (
        float(2.0 * (global_precision * global_recall) / (global_precision + global_recall))
        if (global_precision + global_recall) > 0.0
        else 0.0
    )

    # 3. Weighted F1
    weighted_f1 = float(np.sum(f1_scores * class_supports) / n_samples)

    return macro_f1, micro_f1, weighted_f1
