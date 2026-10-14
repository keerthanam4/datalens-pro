
"""Calculate an explainable heuristic data-quality score."""

import pandas as pd


def calculate_quality_score(df: pd.DataFrame) -> dict:
    """Score data quality from 0 to 100 using missing and duplicate rates.

    Missing cells account for 70% of the score.
    Duplicate rows account for 30% of the score.

    This is a project-specific heuristic, not a universal quality standard.
    """
    if df is None:
        raise ValueError("A DataFrame is required.")

    rows, columns = df.shape
    total_cells = rows * columns

    missing_rate = (
        float(df.isna().sum().sum() / total_cells)
        if total_cells
        else 0.0
    )

    duplicate_rate = (
        float(df.duplicated().sum() / rows)
        if rows
        else 0.0
    )

    missing_component = 100 * (1 - missing_rate)
    duplicate_component = 100 * (1 - duplicate_rate)

    score = round(
        0.7 * missing_component + 0.3 * duplicate_component,
        2,
    )

    return {
        "score": score,
        "grade": (
            "Excellent" if score >= 90
            else "Good" if score >= 75
            else "Fair" if score >= 50
            else "Needs attention"
        ),
        "missing_rate_percent": round(missing_rate * 100, 2),
        "duplicate_rate_percent": round(duplicate_rate * 100, 2),
        "weights": {
            "missing_values": 70,
            "duplicate_rows": 30,
        },
    }
