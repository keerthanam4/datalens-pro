
import pandas as pd
import pytest

from analyzer.quality import analyze_quality


def test_detects_missing_values():
    df = pd.DataFrame({
        "name": ["Asha", None, "Ravi"],
        "age": [22, 25, None],
    })

    report = analyze_quality(df)

    assert report["missing_cell_count"] == 2
    assert report["missing_values"]["name"]["count"] == 1
    assert report["missing_values"]["age"]["count"] == 1


def test_detects_duplicate_rows():
    df = pd.DataFrame({
        "name": ["Asha", "Ravi", "Asha"],
        "age": [22, 25, 22],
    })

    report = analyze_quality(df)

    assert report["duplicate_row_count"] == 1


def test_reports_column_properties():
    df = pd.DataFrame({"city": ["Hyderabad", "Chennai", "Hyderabad"]})

    report = analyze_quality(df)

    assert report["row_count"] == 3
    assert report["column_count"] == 1
    assert report["columns"]["city"]["unique_count"] == 2


def test_rejects_missing_dataframe():
    with pytest.raises(ValueError, match="DataFrame"):
        analyze_quality(None)

def test_profile_numeric_and_categorical_columns():
    from analyzer.profiler import profile_columns

    df = pd.DataFrame({
        "age": [20, 30, 40],
        "city": ["Hyderabad", "Chennai", "Hyderabad"],
    })

    result = profile_columns(df)

    assert result["age"]["inferred_type"] == "numeric"
    assert result["age"]["mean"] == 30.0
    assert result["city"]["inferred_type"] == "categorical"
    assert result["city"]["unique_count"] == 2

def test_quality_score_for_perfect_data():
    from analyzer.scoring import calculate_quality_score

    df = pd.DataFrame({"name": ["Asha", "Ravi"], "age": [20, 25]})

    result = calculate_quality_score(df)

    assert result["score"] == 100.0
    assert result["grade"] == "Excellent"


def test_quality_score_penalizes_missing_values():
    from analyzer.scoring import calculate_quality_score

    df = pd.DataFrame({"age": [20, None]})

    result = calculate_quality_score(df)

    assert result["score"] == 65.0
    assert result["missing_rate_percent"] == 50.0
