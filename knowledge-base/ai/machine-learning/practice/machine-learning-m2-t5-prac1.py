import pandas as pd


def custom_target_encoder(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    cat_col: str,
    target_col: str,
    smoothing: float,
) -> tuple[pd.Series, pd.Series]:
    """Applies target encoding with Laplace smoothing to training and validation sets.

    Crucial:
    1. Statistics must be fit ONLY on train_df to prevent leakage.
    2. Categories in val_df not present in train_df must fall back to the
       global train target mean.
    """
    global_mean = train_df[target_col].mean()

    # Calculate statistics from training set
    stats = train_df.groupby(cat_col)[target_col].agg(["count", "mean"])
    counts = stats["count"]
    means = stats["mean"]

    # Compute weights and smoothed mapping
    weights = counts / (counts + smoothing)
    smoothed_mapping = weights * means + (1 - weights) * global_mean

    # Transform training and validation data
    train_encoded = train_df[cat_col].map(smoothed_mapping).fillna(global_mean)
    val_encoded = val_df[cat_col].map(smoothed_mapping).fillna(global_mean)

    return train_encoded, val_encoded
