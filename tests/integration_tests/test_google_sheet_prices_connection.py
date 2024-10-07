import pytest
import json
import gspread
from google.oauth2.service_account import Credentials
import re

def test_google_sheet_prices_connection():
    # Load Google Sheets credentials
    creds_path = "/home/juaneshberger/Credentials/gdrive_credentials.json"
    with open(creds_path, 'r') as file:
        gdrive_creds = json.load(file)

    # Load Google Sheets URLs
    sheets_creds_path = "/home/juaneshberger/Credentials/spx_sheets.toml"
    with open(sheets_creds_path, 'r') as f:
        lines = f.read()
    
    prices_sheet_url = re.search(r"prices_gdrive\s*=\s*\'(.+?)\'", lines).group(1)

    try:
        creds = Credentials.from_service_account_info(gdrive_creds, scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
        client = gspread.authorize(creds)
        sheet = client.open_by_url(prices_sheet_url).sheet1
        assert sheet.title is not None
    except Exception as e:
        pytest.fail(f"Failed to connect to Google Sheet (Prices): {str(e)}")
