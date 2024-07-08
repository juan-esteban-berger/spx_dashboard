import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import yfinance as yf
from tqdm import tqdm
from datetime import datetime

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
source_sheet = client.open_by_url(source_sheet_url).worksheet('Sheet1')
df_symbols = pd.DataFrame(source_sheet.get_all_records())

if 'symbol' in df_symbols.columns:
    df_symbols.rename(columns={'symbol': 'ticker'}, inplace=True)
symbols_list = df_symbols['ticker'].tolist()

##########################################################################################
# Get Quarterly Financials from Yahoo Finance
sheet_url = os.getenv('SPX_FINANCIALS_GDRIVE')

print("Sourcing financials...")
df_fundamentals = pd.DataFrame()

for ticker in tqdm(symbols_list):
    try:
        stock = yf.Ticker(ticker)
        df_temp = stock.quarterly_financials.transpose().reset_index()
        df_temp['ticker'] = ticker
        df_melt = pd.melt(df_temp, id_vars=['ticker', 'index'], var_name='Metric', value_name='Value')
        df_fundamentals = pd.concat([df_fundamentals, df_melt], ignore_index=True)
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")

##########################################################################################
# Transform Data
print("Preparing data for load...")
df_fundamentals = df_fundamentals.rename(columns={'index': 'Date'})
df_fundamentals['Date'] = pd.to_datetime(df_fundamentals['Date']).dt.strftime('%Y-%m-%d')

##########################################################################################
# Load Data to Target Sheet
print("Clearing old data in target sheet...")
sheet = client.open_by_url(sheet_url).get_worksheet(0)
sheet.clear()

print("Writing new data to target sheet...")
values = df_fundamentals.fillna("").values.tolist()
values.insert(0, df_fundamentals.columns.tolist())
sheet.resize(rows=df_fundamentals.shape[0]+1)
sheet.insert_rows(values, row=1)

print("Update successful, data now available in Google Sheets!")
