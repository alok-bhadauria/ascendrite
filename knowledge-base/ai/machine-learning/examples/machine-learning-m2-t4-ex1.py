import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit


def calculate_vif(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the Variance Inflation Factor (VIF) for each feature

    in the DataFrame to identify multicollinearity.
    """
    features = df.columns
    vif_data = pd.DataFrame()
    vif_data["Feature"] = features
    vifs = []

    for target in features:
        # Separate predictors and target
        predictors = [f for f in features if f != target]
        X = df[predictors]
        y = df[target]

        # Fit auxiliary regression
        model = LinearRegression()
        model.fit(X, y)

        # Calculate R^2
        r_squared = model.score(X, y)

        # Calculate VIF
        if r_squared == 1.0:
            vif = np.inf
        else:
            vif = 1.0 / (1.0 - r_squared)
        vifs.append(vif)

    vif_data["VIF"] = vifs
    return vif_data


def time_series_split_indices(
    n_samples: int, n_splits: int
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Generates time-series split training and validation indices

    to prevent timeline leakage.
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    splits = []
    # Generate dummy array for index generation
    dummy_data = np.zeros(n_samples)

    for train_index, val_index in tscv.split(dummy_data):
        splits.append((train_index, val_index))

    return splits
