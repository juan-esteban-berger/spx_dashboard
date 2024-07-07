import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import yfinance as yf
from tqdm import tqdm
from datetime import datetime, timedelta

##########################################################################################
# Setup Credentials
print("Setting up credentials...")
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds_data = json.loads(os.getenv('JSON_CREDS'))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scopes=scope)

print("Authorizing client...")
client = gspread.authorize(creds)

##########################################################################################
# Get Symbols from Source Sheet
print("Reading symbols from source sheet...")
source_sheet_url = os.getenv('SPX_INFO_GDRIVE')
source_sheet = client.open_by_url(source_sheet_url).get_worksheet(0)
df_symbols = pd.DataFrame(source_sheet.get_all_records())

if 'symbol' in df_symbols.columns:
    df_symbols.rename(columns={'symbol': 'ticker'}, inplace=True)
symbols_list = df_symbols['ticker'].tolist()

##########################################################################################
# Get Prices from Yahoo Finance
sheet_url = os.getenv('SPX_PRICES_GDRIVE')

print("Sourcing prices...")
end_date = datetime.utcnow() - timedelta(days=1)
start_date = end_date - timedelta(days=365)
df_prices = pd.DataFrame()

for ticker in tqdm(symbols_list):
    try:
        df_temp = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), auto_adjust=True)
        df_temp['Ticker'] = ticker
        df_melt = pd.melt(df_temp.reset_index(), id_vars=['Date', 'Ticker'], var_name='Metric', value_name='Value')
        # Drop values where Metric is not Close
        df_melt = df_melt[df_melt['Metric'] == 'Close']
        df_prices = pd.concat([df_prices, df_melt], ignore_index=True)
        # Drop the Metric column
        df_prices.drop(columns=['Metric'], inplace=True)
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")

##########################################################################################
# Transform Data
print("Transforming data...")
df_prices['Date'] = pd.to_datetime(df_prices['Date']).dt.strftime('%Y-%m-%d')

##########################################################################################
# Load Data to Target Sheet
print("Clearing old data in target sheet...")
sheet = client.open_by_url(sheet_url).get_worksheet(0)
sheet.clear()

print("Writing new data to target sheet...")
values = df_prices.fillna("").values.tolist()
values.insert(0, df_prices.columns.tolist())
sheet.insert_rows(values, row=1)

print("Update successful, data loaded into Google Sheets!")
