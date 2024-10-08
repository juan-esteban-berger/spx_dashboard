import warnings
warnings.filterwarnings('ignore')
import os
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from data_fetcher import fetch_quarterly_financials_gdrive

def etl_quarterly_financials_gdrive():
    """
    Perform ETL process for quarterly financials and store in Google Sheets.

    This function extracts data using the fetch_quarterly_financials_gdrive function,
    transforms it as needed, and loads it into a Google Sheet.

    Raises:
        Exception: If there's an error in the ETL process
    """
    try:
        # Setup Credentials
        print("Setting up credentials...")
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds_data = json.loads(os.getenv('JSON_CREDS'))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scopes=scope)
        print("Authorizing client...")
        client = gspread.authorize(creds)

        # Get Symbols from Source Sheet
        print("Reading symbols from source sheet...")
        source_sheet_url = os.getenv('SPX_INFO_GDRIVE')
        source_sheet = client.open_by_url(source_sheet_url).worksheet('Sheet1')
        df_symbols = pd.DataFrame(source_sheet.get_all_records())
        if 'symbol' in df_symbols.columns:
            df_symbols.rename(columns={'symbol': 'ticker'}, inplace=True)
        symbols_list = df_symbols['ticker'].tolist()

        # Get Quarterly Financials from Yahoo Finance
        print("Sourcing financials...")
        df_fundamentals = fetch_quarterly_financials_gdrive(symbols_list)

        # Load Data to Target Sheet
        sheet_url = os.getenv('SPX_FINANCIALS_GDRIVE')
        print("Clearing old data in target sheet...")
        sheet = client.open_by_url(sheet_url).get_worksheet(0)
        sheet.clear()
        print("Writing new data to target sheet...")
        values = df_fundamentals.fillna("").values.tolist()
        values.insert(0, df_fundamentals.columns.tolist())
        sheet.resize(rows=df_fundamentals.shape[0]+1)
        sheet.insert_rows(values, row=1)
        print("Update successful, data now available in Google Sheets!")

    except Exception as e:
        print(f"Error in ETL process: {str(e)}")
        raise

if __name__ == "__main__":
    etl_quarterly_financials_gdrive()
