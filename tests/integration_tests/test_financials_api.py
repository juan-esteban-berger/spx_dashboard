import pytest
import requests
import pandas as pd
from datetime import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def test_financials_api_connection():
    """Test connection and data quality for Financials API endpoint"""
    api_url_path = "/home/juaneshberger/Credentials/spx-django.txt"
    with open(api_url_path, 'r') as f:
        api_url = f.read().strip()
    
    print("\n=== Testing S&P 500 Financials API ===")
    base_url = f"{api_url}api/financials"
    
    try:
        # Test 1: Basic API Connection with Limit
        print("\n1. Testing basic API connection...")
        response = requests.get(f"{base_url}/?limit=10")
        assert response.status_code == 200
        data = response.json()
        df = pd.DataFrame(data)
        print("\nSample financial records:")
        print(df.to_string())
        
        # Test 2: Data Structure Validation
        print("\n2. Validating data structure...")
        expected_columns = {'ticker', 'date', 'variable', 'value'}
        missing_cols = expected_columns - set(df.columns)
        assert not missing_cols, f"Missing columns: {missing_cols}"
        
        # Test 3: Financial Variables Analysis
        print("\n3. Analyzing financial variables...")
        print("\nUnique financial variables:")
        variables = df['variable'].unique()
        print(pd.Series(variables).to_string())
        
        # Test 4: Testing Symbol Filter
        print("\n4. Testing symbol filter...")
        test_ticker = df['ticker'].iloc[0]
        symbol_response = requests.get(f"{base_url}/?symbols[]={test_ticker}&limit=5")
        assert symbol_response.status_code == 200
        symbol_df = pd.DataFrame(symbol_response.json())
        print(f"\nFinancial records for {test_ticker}:")
        print(symbol_df.to_string())
        
        # Test 5: Value Range Analysis
        print("\n5. Analyzing value ranges...")
        print("\nSummary statistics for financial values:")
        print(df.groupby('variable')['value'].describe())
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
