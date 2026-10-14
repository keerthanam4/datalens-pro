
import pandas as pd
import pytest

from analyzer.outliers import detect_outliers


def test_detects_extreme_value():
    df = pd.DataFrame({"salary": [10, 11, 12, 13, 14, 100]})

    result = detect_outliers(df)

    assert result["salary"]["outlier_count"] == 1
    assert result["salary"]["outlier_values"] == [100]


def test_no_outliers_in_constant_column():
    df = pd.DataFrame({"score": [5, 5, 5, 5]})

    result = detect_outliers(df)

    assert result["score"]["outlier_count"] == 0


def test_rejects_missing_dataframe():
    with pytest.raises(ValueError, match="DataFrame"):
        detect_outliers(None)
