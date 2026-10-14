
import pandas as pd
import pytest

from analyzer.cleaning import clean_data


def test_remove_duplicate_rows():
    df = pd.DataFrame({"name": ["Asha", "Asha", "Ravi"]})

    result = clean_data(df, remove_duplicates=True)

    assert len(result) == 2
    assert len(df) == 3  # Original remains unchanged.


def test_fill_numeric_missing_values_with_mean():
    df = pd.DataFrame({"score": [10.0, None, 30.0]})

    result = clean_data(df, fill_missing="mean")

    assert result["score"].isna().sum() == 0
    assert result.loc[1, "score"] == 20.0


def test_drop_rows_with_missing_values():
    df = pd.DataFrame({"name": ["Asha", None], "age": [20, 30]})

    result = clean_data(df, fill_missing="drop_rows")

    assert len(result) == 1


def test_reject_invalid_cleaning_option():
    with pytest.raises(ValueError, match="fill_missing"):
        clean_data(pd.DataFrame({"x": [1]}), fill_missing="invalid")

def test_original_dataframe_is_not_modified():
    df = pd.DataFrame({"age": [20.0, None, 30.0]})
    original = df.copy(deep=True)

    cleaned = clean_data(df, fill_missing="mean")

    pd.testing.assert_frame_equal(df, original)
    assert cleaned.loc[1, "age"] == 25.0


def test_all_missing_numeric_column_remains_missing():
    df = pd.DataFrame({"age": [None, None]})

    cleaned = clean_data(df, fill_missing="mean")

    assert cleaned["age"].isna().all()


def test_mode_fills_numeric_and_categorical_columns():
    df = pd.DataFrame({
        "age": [20.0, None, 20.0, 30.0],
        "city": ["Hyderabad", None, "Hyderabad", "Chennai"],
    })

    cleaned = clean_data(df, fill_missing="mode")

    assert cleaned.loc[1, "age"] == 20.0
    assert cleaned.loc[1, "city"] == "Hyderabad"


def test_mean_does_not_fill_categorical_columns():
    df = pd.DataFrame({"city": ["Hyderabad", None, "Chennai"]})

    cleaned = clean_data(df, fill_missing="mean")

    assert cleaned["city"].isna().sum() == 1


def test_median_fills_numeric_missing_values():
    df = pd.DataFrame({"age": [10.0, None, 30.0]})

    cleaned = clean_data(df, fill_missing="median")

    assert cleaned.loc[1, "age"] == 20.0


def test_drop_rows_removes_any_row_with_missing_values():
    df = pd.DataFrame({
        "name": ["Asha", "Ravi", "Meena"],
        "age": [22.0, None, 24.0],
    })

    cleaned = clean_data(df, fill_missing="drop_rows")

    assert len(cleaned) == 2
    assert cleaned.isna().sum().sum() == 0


def test_invalid_remove_duplicates_type_is_rejected():
    df = pd.DataFrame({"age": [20, 20]})

    try:
        clean_data(df, remove_duplicates="yes")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid remove_duplicates")


def test_invalid_dataframe_is_rejected():
    try:
        clean_data(None)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid DataFrame")

def test_trim_whitespace():
    df = pd.DataFrame({"city": [" Hyderabad ", "Chennai "]})

    cleaned = clean_data(df, trim_whitespace=True)

    assert cleaned["city"].tolist() == ["Hyderabad", "Chennai"]


def test_lowercase_text_normalization():
    df = pd.DataFrame({"city": ["Hyderabad", "CHENNAI"]})

    cleaned = clean_data(df, text_case="lower")

    assert cleaned["city"].tolist() == ["hyderabad", "chennai"]


def test_custom_missing_tokens_are_filled_with_mode():
    df = pd.DataFrame({
        "city": ["Hyderabad", "N/A", "Hyderabad", "Chennai"]
    })

    cleaned = clean_data(
        df,
        fill_missing="mode",
        missing_tokens=("N/A", "NULL"),
    )

    assert cleaned.loc[1, "city"] == "Hyderabad"
    assert cleaned.isna().sum().sum() == 0


def test_missing_token_matching_is_case_insensitive():
    df = pd.DataFrame({"city": ["Hyderabad", "n/a", "Chennai"]})

    cleaned = clean_data(
        df,
        fill_missing="drop_rows",
        missing_tokens=("N/A",),
    )

    assert len(cleaned) == 2
    assert "n/a" not in cleaned["city"].tolist()


def test_duplicate_removal_after_text_trimming():
    df = pd.DataFrame({"city": [" Hyderabad ", "Hyderabad"]})

    cleaned = clean_data(
        df,
        trim_whitespace=True,
        remove_duplicates=True,
    )

    assert len(cleaned) == 1


def test_invalid_text_case_is_rejected():
    df = pd.DataFrame({"city": ["Hyderabad"]})

    try:
        clean_data(df, text_case="random")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid text_case")


def test_original_data_is_preserved_with_text_cleaning():
    df = pd.DataFrame({"city": [" Hyderabad ", "N/A"]})
    original = df.copy(deep=True)

    clean_data(
        df,
        trim_whitespace=True,
        fill_missing="drop_rows",
        missing_tokens=("N/A",),
    )

    pd.testing.assert_frame_equal(df, original)
