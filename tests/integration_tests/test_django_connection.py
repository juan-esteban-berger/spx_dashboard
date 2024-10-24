import pytest
import requests

def test_django_api_connection():
    """Test connection to Django API endpoint"""
    # Load Django API URL
    api_url_path = "/home/juaneshberger/Credentials/spx-django.txt"
    with open(api_url_path, 'r') as f:
        api_url = f.read().strip()
    
    print(f"\nTesting API connection to: {api_url}api/info/")
    
    try:
        # Test basic API connection
        response = requests.get(f"{api_url}api/info/")
        print(f"Response status code: {response.status_code}")
        
        # Basic response validation
        assert response.status_code == 200
        data = response.json()
        print(f"Number of records received: {len(data)}")
        assert isinstance(data, list)
        
        # If we got data, check first record structure
        if len(data) > 0:
            first_item = data[0]
            print(f"Sample record: {first_item}")
            assert 'symbol' in first_item
            assert 'security' in first_item
            
    except Exception as e:
        pytest.fail(f"Failed to connect to Django API: {str(e)}")
