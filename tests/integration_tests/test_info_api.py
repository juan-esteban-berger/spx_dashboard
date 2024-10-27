# test_info_api.py
import pytest
import requests
import pandas as pd
from datetime import datetime

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

def test_info_api_connection():
    """Test connection and data quality for Info API endpoint"""
    config = APITestConfig()
    base_url = f"{config.api_url}api/info"
    
    try:
        # Test 1: Basic API Connection
        print("\n1. Testing basic API connection...")
        response = requests.get(f"{base_url}/", headers=config.headers)
        assert response.status_code == 200, "Failed to connect to API"
        
        data = response.json()
        df = pd.DataFrame(data)
        print(f"\nFirst 5 records from Info API:")
        print(df.head().to_string())
        
        # Test 2: Filter Options
        print("\n2. Testing filter options endpoint...")
        filter_response = requests.get(
            f"{base_url}/filter_options/",
            headers=config.headers
        )
        assert filter_response.status_code == 200, "Failed to get filter options"
        filter_data = filter_response.json()
        
        # Test 3: Filtered Data
        print("\n3. Testing filtered queries...")
        # Get sample values from our data
        test_sector = df['gics_sector'].iloc[0]
        test_location = df['headquarters_location'].iloc[0]
        test_founded_min = "1800"  # Example value
        test_founded_max = "2024"  # Example value
        
        filter_url = (f"{base_url}/?sectors[]={test_sector}"
                     f"&locations[]={test_location}"
                     f"&founded_min={test_founded_min}"
                     f"&founded_max={test_founded_max}")
        
        filter_response = requests.get(filter_url, headers=config.headers)
        assert filter_response.status_code == 200, "Failed to get filtered data"
        
        filtered_df = pd.DataFrame(filter_response.json())
        print(f"\nFiltered results:")
        print(f"Number of companies: {len(filtered_df)}")
        if not filtered_df.empty:
            print(filtered_df.head().to_string())
            
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
