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
data_fetcher = importlib.import_module("03_source_financials.data_fetcher")
fetch_quarterly_financials = data_fetcher.fetch_quarterly_financials

def test_fetch_quarterly_financials():
    """
    Test the fetch_quarterly_financials function.

    This test checks if the function returns a DataFrame with the expected structure
    and content for a small set of symbols.
    """
    symbols = ['AAPL', 'GOOGL', 'MSFT']

    # Suppress the specific DeprecationWarning from tqdm
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="tqdm")
        df = fetch_quarterly_financials(symbols)

    # Check if it's a DataFrame
    assert isinstance(df, pd.DataFrame), "Result should be a pandas DataFrame"

    # Check for expected columns
    expected_columns = ['Ticker', 'Date', 'variable', 'value']
    assert all(col in df.columns for col in expected_columns), "DataFrame is missing expected columns"

    # Check if DataFrame is not empty
    assert not df.empty, "DataFrame should not be empty"

    # Check if all requested symbols are present
    assert set(symbols).issubset(set(df['Ticker'])), "Not all requested symbols are present in the result"

    # Check if dates are datetime.date objects
    assert pd.api.types.is_object_dtype(df['Date']), "Date column should be of type object (date)"

    # Check if some common financial metrics are present
    common_metrics = ['Total Revenue', 'Net Income', 'Total Assets', 'Total Liabilities']
    assert any(metric in df['variable'].values for metric in common_metrics), "Common financial metrics are missing"

if __name__ == "__main__":
    pytest.main()
