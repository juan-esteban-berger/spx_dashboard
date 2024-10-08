import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from data_fetcher import fetch_sp500_companies_gdrive

def etl_sp500_info_gdrive():
    """
    Perform ETL process for S&P 500 companies info and store in Google Drive.

    This function extracts data using the fetch_sp500_companies_gdrive function,
    transforms it as needed, and loads it into a Google Sheet.

    Raises:
        Exception: If there's an error in the ETL process
    """
    try:
        # Extract Data
        print("Sourcing data...")
        df_info = fetch_sp500_companies_gdrive()
        print(df_info)

        # Setup Credentials
        print("Setting up credentials...")
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds_data = json.loads(os.getenv('JSON_CREDS'))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scopes=scope)

        # Authorize Client
        print("Authorizing client...")
        client = gspread.authorize(creds)
        sheet_url = os.getenv('SPX_INFO_GDRIVE')

        # Load Data into Google Sheets
        print("Accessing sheet...")
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)
        print("Clearing old data...")
        worksheet.clear()
        print("Writing new data...")
        values = df_info.fillna("").values.tolist()
        values.insert(0, df_info.columns.tolist())
        worksheet.resize(rows=df_info.shape[0]+1)
        worksheet.insert_rows(values, row=1)
        print("Data updated successfully!")

    except Exception as e:
        print(f"Error in ETL process: {str(e)}")
        raise

if __name__ == "__main__":
    etl_sp500_info_gdrive()
