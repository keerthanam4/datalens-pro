# DataLens Pro
### Smart CSV Data Quality & Profiling Platform

**DataLens Pro** is a Python-based web application for exploring CSV datasets, identifying data-quality issues, detecting potential outliers, and preparing cleaned datasets while preserving the original data.

**Live Demo:** https://datalens-pro-ynayn7oa4qveimcy59sku.streamlit.app/  
**GitHub Repository:** https://github.com/keerthanam4/datalens-pro

## Features

- **CSV Upload:** Upload and analyze CSV datasets.
- **Dataset Overview:** View row counts, column counts, missing cells, and duplicate rows.
- **Data Quality Score:** Evaluate dataset completeness and duplicate-row rate using a project-specific scoring method.
- **Column Profiling:** Inspect inferred data types, unique values, common values, and numeric statistics.
- **Missing-Value Analysis:** Identify missing values by column.
- **Duplicate Detection:** Detect duplicate rows.
- **Outlier Detection:** Identify potential numeric outliers using the Interquartile Range (IQR) method.
- **Interactive Charts:** Explore datasets using histograms and other supported charts.
- **Data Cleaning:** Fill missing values using mean, median, or mode, or remove incomplete rows.
- **Text Cleaning:** Trim whitespace and normalize text case.
- **Custom Missing-Value Tokens:** Configure values such as `N/A`, `NULL`, and `unknown` to be treated as missing during cleaning.
- **Cleaned Data Export:** Download cleaned CSV files and JSON quality reports.
- **Before-and-After Comparison:** Compare quality metrics before and after cleaning.

## Technology Stack

- Python 3.12
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
│   ├── reporting.py
│   └── scoring.py
├── components/
│   ├── charts.py
│   └── dashboard.py
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
- Git

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/keerthanam4/datalens-pro.git
cd datalens-pro
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows:**

```bat
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

http://localhost:8501

## Run Tests

```bash
python -m pytest -v
```

The local test suite previously completed with **33 passing tests**. Run the command above to verify the current version.

## Data Cleaning Workflow

1. Upload a CSV file.
2. Review dataset statistics and data-quality metrics.
3. Configure missing-value handling and text-cleaning options.
4. Preview the cleaning results.
5. Compare original and cleaned quality metrics.
6. Download the cleaned CSV or JSON quality report.

Cleaning operations work on a separate DataFrame copy so the original uploaded DataFrame is preserved.

## Notes and Limitations

- The quality score is a project-specific heuristic, not a universal data-quality standard.
- IQR outliers are potential anomalies and may represent valid observations.
- Mean and median imputation apply to numeric columns; mode imputation can also be used for categorical data.
- Custom missing-value tokens are applied during the cleaning workflow.

## Future Improvements

- Configurable outlier-handling strategies.
- Additional data-validation rules.
- More detailed cleaning audit reports.
- Expanded automated test coverage.

## License

No license has been specified yet. Add a license file if you intend to distribute the project under a particular open-source license.
