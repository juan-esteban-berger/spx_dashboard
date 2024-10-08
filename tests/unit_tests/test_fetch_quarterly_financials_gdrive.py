import pytest
import pandas as pd
import sys
from pathlib import Path
import warnings

# Add the project root directory to the Python path
project_root = Path(__file__).parents[2]
sys.path.append(str(project_root))

# Use importlib to import from a directory with a numeric prefix
import importlib
data_fetcher = importlib.import_module("13_source_financials_gdrive.data_fetcher")
fetch_quarterly_financials_gdrive = data_fetcher.fetch_quarterly_financials_gdrive

def test_fetch_quarterly_financials_gdrive():
    """
    Test the fetch_quarterly_financials_gdrive function.

    This test checks if the function returns a DataFrame with the expected structure
    and content for a small set of symbols.
    """
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    
    # Suppress warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        df = fetch_quarterly_financials_gdrive(symbols)

    # Check if it's a DataFrame
    assert isinstance(df, pd.DataFrame), "Result should be a pandas DataFrame"

    # Check for expected columns
    expected_columns = ['ticker', 'Date', 'Metric', 'Value']
    assert all(col in df.columns for col in expected_columns), "DataFrame is missing expected columns"

    # Check if DataFrame is not empty
    assert not df.empty, "DataFrame should not be empty"

    # Check if all requested symbols are present
    assert set(symbols).issubset(set(df['ticker'])), "Not all requested symbols are present in the result"

    # Check if dates are in the correct format
    assert df['Date'].dtype == object, "Date column should be of type object"
    assert df['Date'].str.match(r'\d{4}-\d{2}-\d{2}').all(), "Dates should be in YYYY-MM-DD format"

    # Check if some common financial metrics are present
    common_metrics = ['Total Revenue', 'Net Income', 'Total Assets', 'Total Liabilities']
    assert any(metric in df['Metric'].values for metric in common_metrics), "Common financial metrics are missing"

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        pytest.main()
