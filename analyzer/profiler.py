
"""Generate descriptive profiles for DataFrame columns."""

import pandas as pd


def profile_columns(df: pd.DataFrame) -> dict:
    """Return data types, missing values, and useful statistics per column."""
    if df is None:
        raise ValueError("A DataFrame is required.")

    profiles = {}

    for column in df.columns:
        series = df[column]
        numeric = pd.to_numeric(series, errors="coerce")
        non_missing = series.dropna()

        # Classify a column as numeric only when all non-missing values
        # can be interpreted as numbers.
        is_numeric = (
            len(non_missing) > 0
            and numeric[series.notna()].notna().all()
        )

        if is_numeric:
            profiles[str(column)] = {
                "inferred_type": "numeric",
                "missing_count": int(series.isna().sum()),
                "unique_count": int(series.nunique()),
                "minimum": float(numeric.min()),
                "maximum": float(numeric.max()),
                "mean": round(float(numeric.mean()), 2),
                "median": float(numeric.median()),
                "standard_deviation": (
                    round(float(numeric.std()), 2)
                    if len(non_missing) > 1
                    else 0.0
                ),
            }
        else:
            profiles[str(column)] = {
                "inferred_type": "categorical",
                "missing_count": int(series.isna().sum()),
                "unique_count": int(series.nunique()),
                "most_common": (
                    str(series.mode().iloc[0])
                    if not series.mode().empty
                    else None
                ),
            }

    return profiles
