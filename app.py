
"""DataLens Pro — Smart CSV Data Quality & Profiling Platform."""

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from analyzer.cleaning import clean_data
from analyzer.loader import load_csv
from analyzer.outliers import detect_outliers
from analyzer.profiler import profile_columns
from analyzer.quality import analyze_quality
from analyzer.scoring import calculate_quality_score


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="DataLens Pro",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 DataLens Pro")
st.caption("Smart CSV Data Quality & Profiling Platform")

st.markdown(
    "Upload a CSV to inspect data quality, profile columns, "
    "identify potential outliers, and safely prepare a cleaned copy."
)


# ---------------------------------------------------------
# CSV upload and validation
# ---------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"],
    help="Your dataset is processed in this app session.",
)

if uploaded_file is None:
    st.info("Upload a CSV file to start your analysis.")
    st.stop()

try:
    df = load_csv(uploaded_file)
except Exception as exc:
    st.error(f"Could not read the CSV: {exc}")
    st.stop()

if df.empty:
    st.warning("This CSV has column headers but no data rows.")
    st.dataframe(df, use_container_width=True)
    st.stop()


# ---------------------------------------------------------
# Dataset analysis
# ---------------------------------------------------------
try:
    quality = analyze_quality(df)
    score = calculate_quality_score(df)
    profiles = profile_columns(df)
    outliers = detect_outliers(df)
except Exception as exc:
    st.error(f"Could not analyze the dataset: {exc}")
    st.stop()


# ---------------------------------------------------------
# Dataset overview
# ---------------------------------------------------------
st.divider()
st.subheader("Dataset overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", f"{quality['row_count']:,}")
col2.metric("Columns", f"{quality['column_count']:,}")
col3.metric("Missing cells", f"{quality['missing_cell_count']:,}")
col4.metric("Duplicate rows", f"{quality['duplicate_row_count']:,}")

score_col, details_col = st.columns([1, 2])

with score_col:
    st.subheader("Data quality score")
    st.metric(
        "Score",
        f"{score['score']:.1f}/100",
        score["grade"],
    )
    st.progress(max(0.0, min(1.0, score["score"] / 100)))
    st.caption(
        "Heuristic score: 70% missing-value completeness "
        "and 30% duplicate-row rate."
    )

with details_col:
    st.subheader("Column profiles")
    profile_df = pd.DataFrame.from_dict(profiles, orient="index")
    profile_df.index.name = "Column"
    st.dataframe(profile_df, use_container_width=True)


# ---------------------------------------------------------
# Data preview
# ---------------------------------------------------------
st.divider()
st.subheader("Data preview")

st.dataframe(df.head(100), use_container_width=True)
st.caption(f"Showing up to 100 of {len(df):,} rows.")


# ---------------------------------------------------------
# Missing-value analysis
# ---------------------------------------------------------
st.divider()
st.subheader("Missing values")

missing_df = pd.DataFrame.from_dict(
    quality["missing_values"],
    orient="index",
)
missing_df.index.name = "Column"
missing_df = missing_df.rename(
    columns={
        "count": "Missing count",
        "percentage": "Missing %",
    }
)

st.dataframe(missing_df, use_container_width=True)

if quality["missing_cell_count"] > 0:
    missing_chart = missing_df[
        missing_df["Missing count"] > 0
    ]

    fig = px.bar(
        missing_chart.reset_index(),
        x="Column",
        y="Missing count",
        title="Missing values by column",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.success("No missing values detected.")


# ---------------------------------------------------------
# Duplicate-row analysis
# ---------------------------------------------------------
st.divider()
st.subheader("Duplicate rows")

st.write(
    f"Detected **{quality['duplicate_row_count']}** duplicate rows."
)


# ---------------------------------------------------------
# Outlier analysis
# ---------------------------------------------------------
st.divider()
st.subheader("Potential outliers")

outlier_rows = []

for column, result in outliers.items():
    outlier_rows.append(
        {
            "Column": column,
            "Lower bound": result["lower_bound"],
            "Upper bound": result["upper_bound"],
            "Outlier count": result["outlier_count"],
            "Outlier values": str(result["outlier_values"][:10]),
        }
    )

if outlier_rows:
    st.dataframe(
        pd.DataFrame(outlier_rows),
        use_container_width=True,
    )
else:
    st.info("No numeric columns are available for IQR outlier detection.")

st.caption(
    "Outliers are potential anomalies, not necessarily incorrect values."
)


# ---------------------------------------------------------
# Interactive chart explorer
# ---------------------------------------------------------
st.divider()
st.subheader("Interactive chart explorer")

numeric_columns = df.select_dtypes(include="number").columns.tolist()
all_columns = df.columns.tolist()

if numeric_columns:
    chart_type = st.selectbox(
        "Chart type",
        ["Histogram", "Box plot", "Scatter plot", "Bar chart"],
        key="chart_type",
    )

    fig = None

    if chart_type in ["Histogram", "Box plot"]:
        selected_column = st.selectbox(
            "Choose a numeric column",
            numeric_columns,
            key="distribution_column",
        )

        if chart_type == "Histogram":
            fig = px.histogram(
                df,
                x=selected_column,
                title=f"Distribution of {selected_column}",
            )
        else:
            fig = px.box(
                df,
                y=selected_column,
                title=f"Box plot of {selected_column}",
            )

    elif chart_type == "Scatter plot":
        if len(numeric_columns) < 2:
            st.warning(
                "A scatter plot requires at least two numeric columns."
            )
        else:
            x_column = st.selectbox(
                "X-axis",
                numeric_columns,
                key="scatter_x",
            )

            y_options = [
                column
                for column in numeric_columns
                if column != x_column
            ]

            y_column = st.selectbox(
                "Y-axis",
                y_options,
                key="scatter_y",
            )

            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=f"{y_column} vs {x_column}",
            )

    else:
        category_options = [
            column
            for column in all_columns
            if column not in numeric_columns
        ] or all_columns

        category_column = st.selectbox(
            "Category",
            category_options,
            key="bar_category",
        )

        value_column = st.selectbox(
            "Numeric value",
            numeric_columns,
            key="bar_value",
        )

        grouped = (
            df.groupby(category_column, dropna=False)[value_column]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            grouped.head(50),
            x=category_column,
            y=value_column,
            title=f"Average {value_column} by {category_column}",
        )

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No numeric columns found for the available charts.")


# ---------------------------------------------------------
# Safe cleaning workspace
# ---------------------------------------------------------
st.divider()
st.subheader("Safe cleaning workspace")

st.write(
    "Cleaning creates a separate copy. "
    "The uploaded dataset remains unchanged."
)

with st.form("cleaning_form"):
    remove_duplicates = st.checkbox(
        "Remove duplicate rows from the cleaned copy",
        key="remove_duplicates_option",
    )

    fill_option = st.selectbox(
        "How should missing values be handled?",
        ["none", "mean", "median", "mode", "drop_rows"],
        format_func=lambda option: {
            "none": "Leave missing values unchanged",
            "mean": "Fill numeric columns with mean",
            "median": "Fill numeric columns with median",
            "mode": "Fill with most frequent value",
            "drop_rows": "Remove rows containing missing values",
        }[option],
        key="fill_missing_option",
    )

    st.markdown("**Text cleaning options**")

    trim_whitespace = st.checkbox(
        "Trim leading and trailing whitespace",
        key="trim_whitespace_option",
    )

    text_case = st.selectbox(
        "Text case normalization",
        ["preserve", "lower", "upper", "title"],
        format_func=lambda option: {
            "preserve": "Preserve original case",
            "lower": "Convert to lowercase",
            "upper": "Convert to UPPERCASE",
            "title": "Convert To Title Case",
        }[option],
        key="text_case_option",
    )

    missing_tokens_input = st.text_input(
        "Custom missing-value tokens (comma-separated)",
        value="N/A, NULL, unknown",
        help=(
            "These tokens are treated as missing, ignoring case "
            "and surrounding spaces."
        ),
        key="missing_tokens_input",
    )

    preview_clicked = st.form_submit_button(
        "Preview cleaning",
        type="primary",
    )


# ---------------------------------------------------------
# Execute cleaning only when the form is submitted
# ---------------------------------------------------------
if preview_clicked:
    missing_tokens = tuple(
        token.strip()
        for token in missing_tokens_input.split(",")
        if token.strip()
    )

    try:
        cleaned = clean_data(
            df,
            remove_duplicates=remove_duplicates,
            fill_missing=fill_option,
            trim_whitespace=trim_whitespace,
            text_case=text_case,
            missing_tokens=missing_tokens,
        )

        st.session_state["cleaned_data"] = cleaned
        st.session_state["cleaning_source"] = uploaded_file.name
        st.session_state["cleaning_options"] = {
            "remove_duplicates": remove_duplicates,
            "fill_missing": fill_option,
            "trim_whitespace": trim_whitespace,
            "text_case": text_case,
            "missing_tokens": list(missing_tokens),
        }

    except (ValueError, TypeError, KeyError) as exc:
        st.error(f"Could not clean the dataset: {exc}")
        st.stop()


# ---------------------------------------------------------
# Cleaned-data preview and downloads
# ---------------------------------------------------------
if (
    "cleaned_data" in st.session_state
    and st.session_state.get("cleaning_source") == uploaded_file.name
):
    cleaned = st.session_state["cleaned_data"]

    st.divider()
    st.subheader("Cleaning results")

    original_rows = len(df)
    cleaned_rows = len(cleaned)
    rows_removed = original_rows - cleaned_rows

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Original rows", f"{original_rows:,}")
    metric2.metric("Cleaned rows", f"{cleaned_rows:,}")
    metric3.metric("Rows removed", f"{rows_removed:,}")

    st.metric(
        "Remaining duplicate rows",
        int(cleaned.duplicated().sum()),
    )

    st.dataframe(
        cleaned.head(100),
        use_container_width=True,
    )

    # Before-and-after quality comparison.
    cleaned_quality = analyze_quality(cleaned)
    cleaned_score = calculate_quality_score(cleaned)

    with st.expander("Before-and-after quality comparison"):
        comparison = pd.DataFrame(
            {
                "Metric": [
                    "Rows",
                    "Columns",
                    "Missing cells",
                    "Duplicate rows",
                    "Quality score",
                ],
                "Original": [
                    quality["row_count"],
                    quality["column_count"],
                    quality["missing_cell_count"],
                    quality["duplicate_row_count"],
                    round(score["score"], 2),
                ],
                "Cleaned": [
                    cleaned_quality["row_count"],
                    cleaned_quality["column_count"],
                    cleaned_quality["missing_cell_count"],
                    cleaned_quality["duplicate_row_count"],
                    round(cleaned_score["score"], 2),
                ],
            }
        )

        st.dataframe(
            comparison,
            hide_index=True,
            use_container_width=True,
        )

    # Download cleaned CSV.
    st.download_button(
        "Download cleaned CSV",
        data=cleaned.to_csv(index=False).encode("utf-8"),
        file_name="datalens_cleaned.csv",
        mime="text/csv",
        key="download_cleaned_csv",
    )

    # Download detailed JSON report.
    report = {
        "report_type": "cleaned_dataset",
        "original_quality": quality,
        "original_score": score,
        "cleaned_quality": cleaned_quality,
        "cleaned_score": cleaned_score,
        "rows_removed": rows_removed,
        "cleaning_options": st.session_state["cleaning_options"],
    }

    st.download_button(
        "Download cleaned data quality report (JSON)",
        data=json.dumps(
            report,
            indent=2,
            default=str,
        ).encode("utf-8"),
        file_name="datalens_cleaned_quality_report.json",
        mime="application/json",
        key="download_cleaned_report",
    )


st.caption("DataLens Pro | Outlier detection uses the IQR method.")
