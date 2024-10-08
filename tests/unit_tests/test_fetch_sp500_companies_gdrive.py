import pytest
import pandas as pd
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parents[2]
sys.path.append(str(project_root))

# Use importlib to import from a directory with a numeric prefix
import importlib
data_fetcher = importlib.import_module("11_source_info_gdrive.data_fetcher")
fetch_sp500_companies_gdrive = data_fetcher.fetch_sp500_companies_gdrive

def test_fetch_sp500_companies_gdrive():
    """
    Test the fetch_sp500_companies_gdrive function.

    This test checks if the function returns a DataFrame with the expected structure
    and content for Google Drive storage.

    It verifies:
    1. The return value is a DataFrame
    2. The DataFrame has the expected columns
    3. The DataFrame is not empty
    4. The data types of specific columns are correct
    5. The 'symbol' column contains expected S&P 500 tickers
    6. The 'date_added' column is in the correct format
    """
    df = fetch_sp500_companies_gdrive()

    # Check if it's a DataFrame
    assert isinstance(df, pd.DataFrame), "Result should be a pandas DataFrame"

    # Check for expected columns
    expected_columns = ['symbol', 'security', 'gics_sector', 'gics_sub_industry', 
                        'headquarters_location', 'date_added', 'cik', 'founded']
    assert all(col in df.columns for col in expected_columns), "DataFrame is missing expected columns"

    # Check if DataFrame is not empty
    assert not df.empty, "DataFrame should not be empty"

    # Check data types of specific columns
    assert df['symbol'].dtype == object, "Symbol column should be of type object"
    assert df['date_added'].dtype == object, "Date added column should be of type object"

    # Check for presence of some well-known S&P 500 tickers
    assert set(['AAPL', 'MSFT', 'GOOGL']).issubset(set(df['symbol'])), "DataFrame should contain major S&P 500 tickers"

    # Check date_added format
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    assert df['date_added'].str.match(date_pattern).all() or df['date_added'].isnull().all(), "Date added should be in YYYY-MM-DD format or NaT"

if __name__ == "__main__":
    pytest.main()
