import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif


def compute_smoothed_target_encoding(
    df: pd.DataFrame,
    category_col: str,
    target_col: str,
    smoothing_parameter: float,
) -> pd.Series:
    """Computes target encoding with Laplace smoothing to prevent overfitting.

    Formula:
        S_i = lambda(n_i) * mean_y_i + (1 - lambda(n_i)) * mean_y_global
        lambda(n_i) = n_i / (n_i + m)
    """
    global_mean = df[target_col].mean()

    # Calculate count and mean for each category
    category_stats = df.groupby(category_col)[target_col].agg(["count", "mean"])

    counts = category_stats["count"]
    means = category_stats["mean"]

    # Compute weights
    lambda_weights = counts / (counts + smoothing_parameter)

    # Compute smoothed values
    smoothed_values = lambda_weights * means + (1 - lambda_weights) * global_mean

    # Map back to the original series
    return df[category_col].map(smoothed_values)


def select_features_via_mi(
    X: pd.DataFrame, y: pd.Series, n_features_to_select: int
) -> list[str]:
    """Calculates Mutual Information scores and returns the top n features."""
    # Compute MI scores
    mi_scores = mutual_info_classif(X, y, random_state=42)

    # Rank features
    mi_df = pd.DataFrame({"Feature": X.columns, "MI_Score": mi_scores})
    mi_df = mi_df.sort_values(by="MI_Score", ascending=False)

    return mi_df.head(n_features_to_select)["Feature"].tolist()
