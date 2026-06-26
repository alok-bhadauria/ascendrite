import pandas as pd
from sklearn.linear_model import LinearRegression


def get_collinear_features(df: pd.DataFrame, threshold: float) -> list[str]:
    """Identifies and returns features that exceed the VIF threshold.

    Implement:
    1. Auxiliary linear regression of target feature against other columns.
    2. Convert R^2 score into VIF rating.
    3. Return list of feature labels that are greater than threshold.
    """
    collinear_features = []

    for col in df.columns:
        predictors = [c for c in df.columns if c != col]
        X = df[predictors]
        y = df[col]

        model = LinearRegression()
        model.fit(X, y)
        r2 = model.score(X, y)

        if r2 < 1.0:
            vif = 1.0 / (1.0 - r2)
        else:
            vif = float("inf")

        if vif > threshold:
            collinear_features.append(col)

    return collinear_features
