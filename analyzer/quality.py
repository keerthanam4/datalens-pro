
"""Detect common data-quality issues in a DataFrame."""

import pandas as pd


def analyze_quality(df: pd.DataFrame) -> dict:
    """Summarize missing values, duplicate rows, and column properties."""

    if df is None:
        raise ValueError("A DataFrame is required.")

    row_count, column_count = df.shape

    missing_counts = df.isna().sum()
    missing_percentages = (
        (missing_counts / row_count * 100).round(2)
        if row_count > 0
        else missing_counts.astype(float)
    )

    missing_values = {
        str(column): {
            "count": int(missing_counts[column]),
            "percentage": float(missing_percentages[column]),
        }
        for column in df.columns
    }

    duplicate_count = int(df.duplicated().sum())

    columns = {}
    for column in df.columns:
        series = df[column]
        columns[str(column)] = {
            "dtype": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "unique_count": int(series.nunique(dropna=True)),
        }

    total_cells = row_count * column_count
    missing_cell_count = int(missing_counts.sum())

    return {
        "row_count": int(row_count),
        "column_count": int(column_count),
        "missing_cell_count": missing_cell_count,
        "missing_percentage": (
            round(missing_cell_count / total_cells * 100, 2)
            if total_cells
            else 0.0
        ),
        "duplicate_row_count": duplicate_count,
        "missing_values": missing_values,
        "columns": columns,
    }
