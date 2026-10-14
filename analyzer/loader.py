
"""Load and validate CSV files for DataLens Pro."""

from io import BytesIO

import pandas as pd


def load_csv(file) -> pd.DataFrame:
    """Read an uploaded CSV file and return it as a DataFrame.

    Args:
        file: A file-like object, such as a Streamlit uploaded file.

    Returns:
        A pandas DataFrame containing the CSV data.

    Raises:
        ValueError: If the file is empty, malformed, or invalid.
    """
    if file is None:
        raise ValueError("Please upload a CSV file.")

    try:
        # Read from bytes so the loader also works with uploaded files.
        raw_data = file.getvalue() if hasattr(file, "getvalue") else file.read()

        if not raw_data:
            raise ValueError("The uploaded file is empty.")

        # Try common text encodings.
        last_error = None
        for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                df = pd.read_csv(
                    BytesIO(raw_data),
                    encoding=encoding,
                    on_bad_lines="error",
                )
                break
            except UnicodeDecodeError as exc:
                last_error = exc
        else:
            raise ValueError(
                "Could not decode this CSV using supported text encodings."
            ) from last_error

    except pd.errors.EmptyDataError as exc:
        raise ValueError("The CSV contains no readable data.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(
            "The CSV format is invalid. Check the rows and column separators."
        ) from exc

    if df.empty and len(df.columns) == 0:
        raise ValueError("The CSV contains no columns or data.")

    if len(df.columns) == 0:
        raise ValueError("The CSV must contain at least one column.")

    # Make column names unique while preserving the original names in labels.
    original_columns = list(df.columns)
    new_columns = []
    seen = {}

    for column in original_columns:
        name = str(column).strip()

        if not name:
            name = "unnamed_column"

        count = seen.get(name, 0)
        seen[name] = count + 1

        if count:
            name = f"{name}_{count + 1}"

        new_columns.append(name)

    df.columns = new_columns

    return df
