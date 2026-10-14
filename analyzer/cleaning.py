
"""Create cleaned DataFrame copies without modifying the original."""

from typing import Literal

import pandas as pd


FillStrategy = Literal["none", "mean", "median", "mode", "drop_rows"]

ALLOWED_FILL_STRATEGIES = {"none", "mean", "median", "mode", "drop_rows"}
ALLOWED_TEXT_CASES = {"preserve", "lower", "upper", "title"}


def clean_data(
    df: pd.DataFrame,
    *,
    remove_duplicates: bool = False,
    fill_missing: FillStrategy = "none",
    trim_whitespace: bool = False,
    text_case: str = "preserve",
    missing_tokens: tuple[str, ...] = (),
) -> pd.DataFrame:
    """Return a cleaned copy using the selected operations.

    Mean and median affect numeric columns only.
    Mode affects both numeric and categorical columns.
    All-missing columns remain missing when no fill value exists.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("A pandas DataFrame is required.")

    if not isinstance(remove_duplicates, bool):
        raise ValueError("remove_duplicates must be True or False.")

    if not isinstance(trim_whitespace, bool):
        raise ValueError("trim_whitespace must be True or False.")

    if not isinstance(fill_missing, str) or fill_missing not in ALLOWED_FILL_STRATEGIES:
        raise ValueError(
            f"fill_missing must be one of: {sorted(ALLOWED_FILL_STRATEGIES)}"
        )

    if not isinstance(text_case, str) or text_case not in ALLOWED_TEXT_CASES:
        raise ValueError(
            f"text_case must be one of: {sorted(ALLOWED_TEXT_CASES)}"
        )

    if isinstance(missing_tokens, str) or not isinstance(
        missing_tokens, (tuple, list)
    ):
        raise ValueError("missing_tokens must be a list or tuple of strings.")

    if not all(isinstance(token, str) for token in missing_tokens):
        raise ValueError("Every missing-value token must be a string.")

    cleaned = df.copy(deep=True)

    # Convert configured tokens to missing values in text columns.
    tokens = {token.strip().casefold() for token in missing_tokens if token.strip()}

    if tokens:
        for column in cleaned.select_dtypes(include=["object", "string"]).columns:
            values = cleaned[column]
            matches = values.map(
                lambda value: isinstance(value, str)
                and value.strip().casefold() in tokens
            )
            cleaned.loc[matches, column] = pd.NA

    # Normalize text values, without changing non-text values.
    text_columns = cleaned.select_dtypes(include=["object", "string"]).columns

    for column in text_columns:
        values = cleaned[column]

        if trim_whitespace:
            values = values.map(
                lambda value: value.strip() if isinstance(value, str) else value
            )

        if text_case != "preserve":
            if text_case == "lower":
                values = values.map(
                    lambda value: value.lower() if isinstance(value, str) else value
                )
            elif text_case == "upper":
                values = values.map(
                    lambda value: value.upper() if isinstance(value, str) else value
                )
            elif text_case == "title":
                values = values.map(
                    lambda value: value.title() if isinstance(value, str) else value
                )

        cleaned[column] = values

    # Remove duplicates after text normalization so equivalent text rows
    # can become identical before duplicate removal.
    if remove_duplicates:
        cleaned = cleaned.drop_duplicates()

    # Apply the selected missing-value strategy.
    if fill_missing == "drop_rows":
        cleaned = cleaned.dropna()

    elif fill_missing in {"mean", "median"}:
        numeric_columns = cleaned.select_dtypes(include="number").columns

        for column in numeric_columns:
            if cleaned[column].isna().any():
                value = (
                    cleaned[column].mean()
                    if fill_missing == "mean"
                    else cleaned[column].median()
                )

                if pd.notna(value):
                    cleaned[column] = cleaned[column].fillna(value)

    elif fill_missing == "mode":
        for column in cleaned.columns:
            if cleaned[column].isna().any():
                modes = cleaned[column].mode(dropna=True)

                if not modes.empty:
                    cleaned[column] = cleaned[column].fillna(modes.iloc[0])

    return cleaned
