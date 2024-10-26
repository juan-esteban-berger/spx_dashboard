import pytest
import requests
import pandas as pd
from datetime import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def test_prices_api_connection():
    """Test connection and data quality for Prices API endpoint"""
    api_url_path = "/home/juaneshberger/Credentials/spx-django.txt"
    with open(api_url_path, 'r') as f:
        api_url = f.read().strip()
    
    print("\n=== Testing S&P 500 Prices API ===")
    base_url = f"{api_url}api/prices"
    
    try:
        # Test 1: Basic API Connection with Limit
        print("\n1. Testing basic API connection...")
        response = requests.get(f"{base_url}/?limit=5")
        assert response.status_code == 200
        data = response.json()
        df = pd.DataFrame(data)
        print("\nSample price records:")
        print(df.to_string())
        
        # Test 2: Data Structure Validation
        print("\n2. Validating data structure...")
        expected_columns = {'date', 'ticker', 'metric', 'value'}
        missing_cols = expected_columns - set(df.columns)
        assert not missing_cols, f"Missing columns: {missing_cols}"
        
        # Test 3: Testing Ticker Filter
        print("\n3. Testing ticker filter...")
        test_ticker = df['ticker'].iloc[0]
        ticker_response = requests.get(f"{base_url}/by_ticker/?ticker={test_ticker}&limit=5")
        assert ticker_response.status_code == 200
        ticker_df = pd.DataFrame(ticker_response.json())
        print(f"\nPrice records for {test_ticker}:")
        print(ticker_df.to_string())
        
        # Test 4: Metrics Analysis
        print("\n4. Analyzing available metrics...")
        print("\nUnique metrics available:")
        print(df['metric'].unique())
        
        # Test 5: Date Range Validation
        df['date'] = pd.to_datetime(df['date'])
        print("\n5. Analyzing date range...")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
