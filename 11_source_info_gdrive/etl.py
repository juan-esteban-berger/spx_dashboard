import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

##########################################################################################
# Extract Data
print("Sourcing data...")
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
df_info = pd.read_html(url)[0]

##########################################################################################
# Transform Data
df_info['Date added'] = pd.to_datetime(df_info['Date added'])
df_info['Date added'] = df_info['Date added'].apply(lambda x: x.strftime('%Y-%m-%d')) if not df_info['Date added'].isnull().all() else df_info['Date added']
df_info.columns = ['symbol', 'security', 'gics_sector', 'gics_sub_industry', 'headquarters_location', 'date_added', 'cik', 'founded']
df_info['founded'] = df_info['founded'].str.extract(r'(\d+)')
df_info['cik'] = df_info['cik'].astype(str)

print(df_info.head())

##########################################################################################
# Setup Credentials
print("Setting up credentials...")
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds_data = json.loads(os.getenv('JSON_CREDS'))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scopes=scope)

##########################################################################################
# Authorize Client
print("Authorizing client...")
client = gspread.authorize(creds)
sheet_url = 'https://docs.google.com/spreadsheets/d/1O4FdeQOp2KM0YTV6O9JMtzSQyiJ6qDBn5Ng7KSEL4v4/edit?usp=sharing'

##########################################################################################
# Load Data into Google Sheets
print("Accessing sheet...")
sheet = client.open_by_url(sheet_url)
worksheet = sheet.get_worksheet(0)

print("Clearing old data...")
worksheet.clear()

print("Writing new data...")
values = df_info.fillna("").values.tolist()
values.insert(0, df_info.columns.tolist())
worksheet.insert_rows(values, row=1)

print("Data updated successfully!")
