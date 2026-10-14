
from io import BytesIO

import pandas as pd
import pytest

from analyzer.loader import load_csv


def test_load_valid_csv():
    csv_file = BytesIO(b"name,age\nAsha,22\nRavi,25")

    df = load_csv(csv_file)

    assert list(df.columns) == ["name", "age"]
    assert len(df) == 2
    assert df.iloc[0]["name"] == "Asha"


def test_reject_empty_file():
    with pytest.raises(ValueError, match="empty"):
        load_csv(BytesIO(b""))


def test_reject_missing_file():
    with pytest.raises(ValueError, match="upload"):
        load_csv(None)


def test_blank_column_name_is_handled():
    csv_file = BytesIO(b"name, ,age\nAsha,x,22")

    df = load_csv(csv_file)

    assert "unnamed_column" in df.columns
