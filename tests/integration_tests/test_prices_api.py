import pytest
import requests
import pandas as pd
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

class APITestConfig:
    def __init__(self):
        # Read API URL
        api_url_path = "/home/juaneshberger/Credentials/spx-django.txt"
        with open(api_url_path, 'r') as f:
            self.api_url = f.read().strip()
        
        # Read API token
        token_path = "/home/juaneshberger/Credentials/spx-django-token.txt"
        with open(token_path, 'r') as f:
            self.token = f.read().strip()
        
        self.headers = {
            'Authorization': f'Token {self.token}'
        }

def test_prices_api_connection():
    """Test connection and data quality for Prices API endpoint"""
    config = APITestConfig()
    base_url = f"{config.api_url}api/prices"
    
    try:
        # Test 1: Basic API Connection with Limit
        print("\n=== Testing S&P 500 Prices API ===")
        print("\n1. Testing basic API connection...")
        response = requests.get(f"{base_url}/?limit=5", headers=config.headers)
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
        
        # Test 3: Filter Options Endpoint
        print("\n3. Testing filter options endpoint...")
        filter_response = requests.get(
            f"{base_url}/filter_options/",
            headers=config.headers
        )
        assert filter_response.status_code == 200
        filter_data = filter_response.json()
        print("\nAvailable filter options:")
        print(f"Date range: {filter_data['date_range']}")
        print(f"Metrics: {filter_data['metrics']}")
        
        # Test 4: Testing Multiple Filters
        print("\n4. Testing multiple filters...")
        test_ticker = df['ticker'].iloc[0]
        test_metric = df['metric'].iloc[0]
        test_date_min = filter_data['date_range']['min']
        test_date_max = filter_data['date_range']['max']
        
        filter_url = (f"{base_url}/?symbols[]={test_ticker}"
                     f"&metrics[]={test_metric}"
                     f"&date_min={test_date_min}"
                     f"&date_max={test_date_max}"
                     "&limit=5")
        
        filter_response = requests.get(filter_url, headers=config.headers)
        assert filter_response.status_code == 200
        filtered_df = pd.DataFrame(filter_response.json())
        print(f"\nFiltered price records:")
        print(filtered_df.to_string())
        
        # Test 5: Date Range Validation
        print("\n5. Testing date range filter...")
        df['date'] = pd.to_datetime(df['date'])
        print(f"Full date range: {df['date'].min()} to {df['date'].max()}")
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
