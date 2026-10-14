
"""Detect numeric outliers using the interquartile range (IQR)."""

import pandas as pd


def detect_outliers(df: pd.DataFrame) -> dict:
    """Return outlier row indexes and bounds for numeric columns."""
    if df is None:
        raise ValueError("A DataFrame is required.")

    results = {}

    for column in df.select_dtypes(include="number").columns:
        series = df[column].dropna()

        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (
            df[column].notna()
            & ((df[column] < lower_bound) | (df[column] > upper_bound))
        )

        results[str(column)] = {
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "outlier_count": int(mask.sum()),
            "row_indices": df.index[mask].tolist(),
            "outlier_values": df.loc[mask, column].tolist(),
        }

    return results
