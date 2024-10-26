import pytest
import requests
import pandas as pd
from datetime import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def test_info_api_connection():
    """Test connection and data quality for Info API endpoint"""
    api_url_path = "/home/juaneshberger/Credentials/spx-django.txt"
    with open(api_url_path, 'r') as f:
        api_url = f.read().strip()
    
    print("\n=== Testing S&P 500 Info API ===")
    base_url = f"{api_url}api/info"
    
    try:
        # Test 1: Basic API Connection
        print("\n1. Testing basic API connection...")
        response = requests.get(f"{base_url}/")
        assert response.status_code == 200, "Failed to connect to API"
        data = response.json()
        df = pd.DataFrame(data)
        print(f"\nFirst 5 records from Info API:")
        print(df.head().to_string())
        
        # Test 2: Data Structure Validation
        print("\n2. Validating data structure...")
        expected_columns = {'symbol', 'security', 'gics_sector', 'gics_sub_industry', 
                          'headquarters_location', 'date_added', 'cik', 'founded'}
        missing_cols = expected_columns - set(df.columns)
        assert not missing_cols, f"Missing columns: {missing_cols}"
        
        # Test 3: Data Quality Checks
        print("\n3. Performing data quality checks...")
        print(f"\nTotal number of companies: {len(df)}")
        print(f"\nUnique sectors found: {df['gics_sector'].nunique()}")
        print("\nCompanies per sector:")
        print(df['gics_sector'].value_counts().to_string())
        
        # Test 4: Filter Options Endpoint
        print("\n4. Testing filter options endpoint...")
        filter_response = requests.get(f"{base_url}/filter_options/")
        assert filter_response.status_code == 200, "Failed to get filter options"
        filter_data = filter_response.json()
        print("\nAvailable filter options:")
        for key, values in filter_data.items():
            if key == 'founded_range':
                print(f"\n{key}: min={values['min']}, max={values['max']}")
            else:
                print(f"\n{key}: {len(values)} unique values")
                print(f"Sample values: {values[:5]}")
        
        # Test 5: Testing multiple filters
        print("\n5. Testing multiple filters...")
        test_sector = df['gics_sector'].iloc[0]
        test_location = df['headquarters_location'].iloc[0]
        test_founded_min = filter_data['founded_range']['min']
        test_founded_max = filter_data['founded_range']['max']
        
        filter_url = (f"{base_url}/?sectors[]={test_sector}"
                     f"&locations[]={test_location}"
                     f"&founded_min={test_founded_min}"
                     f"&founded_max={test_founded_max}")
        
        filter_response = requests.get(filter_url)
        assert filter_response.status_code == 200
        filtered_df = pd.DataFrame(filter_response.json())
        print(f"\nFiltered results:")
        print(f"Number of companies: {len(filtered_df)}")
        print(filtered_df.head().to_string())

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
