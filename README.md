
# DataLens Pro
### Smart CSV Data Quality & Profiling Platform

DataLens Pro is a Python-based data analysis application that helps users inspect CSV datasets, identify data quality issues, explore columns, detect potential outliers, and prepare cleaned datasets without modifying the original uploaded data.

## Features

- **CSV Upload:** Load and inspect CSV datasets.
- **Dataset Overview:** View row counts, column counts, missing cells, and duplicate rows.
- **Data Quality Score:** Calculate a heuristic score based on missing-value completeness and duplicate-row rate.
- **Column Profiling:** Explore column data types and summary statistics.
- **Missing-Value Analysis:** Identify missing values by column and visualize their distribution.
- **Duplicate Detection:** Identify duplicate rows.
- **Outlier Detection:** Flag potential numeric outliers using the Interquartile Range (IQR) method.
- **Interactive Charts:** Explore data using histograms, box plots, scatter plots, and bar charts.
- **Data Cleaning:** Fill missing values using mean, median, or mode; leave them unchanged; or remove incomplete rows.
- **Text Cleaning:** Trim leading and trailing whitespace and normalize text case.
- **Custom Missing-Value Tokens:** Configure text values such as `N/A`, `NULL`, and `unknown` to be treated as missing during cleaning.
- **Cleaned Data Export:** Download cleaned CSV files and JSON quality reports.
- **Before-and-After Comparison:** Compare original and cleaned dataset quality metrics.

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Pytest

## Project Structure

```text
datalens-pro/
├── analyzer/
│   ├── cleaning.py
│   ├── loader.py
│   ├── outliers.py
│   ├── profiler.py
│   ├── quality.py
│   └── scoring.py
├── components/
├── sample_data/
├── tests/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.12 or a compatible Python version
- pip

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd datalens-pro
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bat
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## Run Tests

```bash
python -m pytest -v
```

The current local test suite contains 33 passing tests.

## Data Cleaning Workflow

1. Upload a CSV file.
2. Review the dataset overview and quality analysis.
3. Select missing-value and text-cleaning options.
4. Preview the cleaned dataset.
5. Review the before-and-after quality comparison.
6. Download the cleaned CSV or JSON quality report.

Cleaning operations create a separate DataFrame copy, preserving the uploaded DataFrame.

## Notes

- The quality score is a project-specific heuristic, not a universal data-quality standard.
- IQR outliers are potential anomalies and may be valid observations.
- Mean and median imputation applies to numeric columns; mode imputation can apply to numeric and categorical columns.
- Custom missing-value tokens are applied during the cleaning workflow.

## Future Improvements

- More configurable outlier treatment.
- Additional data validation rules.
- More detailed cleaning audit reports.
- Expanded automated test coverage.

## License

Add a license if you intend to distribute this project publicly.
