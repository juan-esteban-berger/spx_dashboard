# tests/unit_tests/test_fetch_stock_prices.py

import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path
import warnings

# Add the project root directory to the Python path
project_root = Path(__file__).parents[2]
sys.path.append(str(project_root))

# Use importlib to import from a directory with a numeric prefix
import importlib
data_fetcher = importlib.import_module("02_source_prices.data_fetcher")
fetch_stock_prices = data_fetcher.fetch_stock_prices

def test_fetch_stock_prices():
    """
    Test the fetch_stock_prices function.

    This test checks if the function returns a DataFrame with the expected structure
    and content for a small set of symbols and a short date range.
    """
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=3)

    # Suppress the specific DeprecationWarning from tqdm
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning, module="tqdm")
        df = fetch_stock_prices(symbols, start_date, end_date)

    # Check if it's a DataFrame
    assert isinstance(df, pd.DataFrame), "Result should be a pandas DataFrame"

    # Check for expected columns
    expected_columns = ['Date', 'Ticker', 'Metric', 'Value']
    assert all(col in df.columns for col in expected_columns), "DataFrame is missing expected columns"

    # Check if DataFrame is not empty
    assert not df.empty, "DataFrame should not be empty"

    # Check if all requested symbols are present
    assert set(symbols).issubset(set(df['Ticker'])), "Not all requested symbols are present in the result"

    # Check if date range is correct
    assert df['Date'].min() >= start_date.date(), "Data contains dates earlier than requested"
    assert df['Date'].max() <= end_date.date(), "Data contains dates later than requested"

    # Check if all expected metrics are present
    expected_metrics = ['Open', 'High', 'Low', 'Close', 'Volume']
    assert set(expected_metrics).issubset(set(df['Metric'])), "Not all expected metrics are present"

if __name__ == "__main__":
    pytest.main()
