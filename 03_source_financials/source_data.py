import warnings
warnings.filterwarnings('ignore')

import os
import json
import pandas as pd
import sqlalchemy
import yfinance as yf
from tqdm import tqdm
from datetime import datetime, timedelta

server = os.getenv('server')
port = os.getenv('port')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')

# Create the connection to the database
engine = sqlalchemy.create_engine(f"mssql+pymssql://{user}:{password}@{server}:{port}/{database}")

try:
    ##################################################################
    # Source info
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    df_info = pd.read_html(url)[0]
    df_info['Date added'] = pd.to_datetime(df_info['Date added']).dt.strftime('%Y-%m-%d')

    df_info.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)

    df_info['Headquarters Location'] = df_info['Headquarters Location'].str.replace('"', '')
    df_info['Headquarters Location'] = df_info['Headquarters Location'].str.replace(';', ',')

    # Rename columns
    df_info.columns = ['Symbol', 'Security', 'GICS_Sector', 'GICS_Sub_Industry', 'Headquarters_Location', 'Date_added', 'CIK', 'Founded']

    # If the value of founded contains a parenthesis,
    # then only keepthe numbers insdie the parenthesis
    df_info['Founded'] = df_info['Founded'].str.extract(r'(\d+)')

    print(df_info)

    delete_query = "DELETE FROM StockData.spx.info"

    with engine.connect() as connection:
        connection.execute(delete_query)
        print("Data deleted successfully")


    # Insert data into the database
    df_info = df_info.head(2000)
    df_info.to_sql('info', engine, schema='spx', if_exists='append', index=False)
    print("Data inserted successfully!")

    ##################################################################
    # Source prices
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=10*365)

    df_prices = pd.DataFrame()

    # For now only first 10 tickers
    for ticker in tqdm(df_info['Symbol'].to_list()[:10]):
    # for ticker in tqdm(df_info['Symbol'].to_list()):
        try:
            df_temp = yf.download(ticker,
                                     start=start_date.strftime('%Y-%m-%d'),
                                     end=end_date.strftime('%Y-%m-%d'),
                                     auto_adjust=True)
            df_temp['Ticker'] = ticker
            
            df_melt = pd.melt(df_temp.reset_index(),
                                  id_vars=['Date', 'Ticker'],
                                  var_name='Metric',
                                  value_name='Value')
            df_prices = pd.concat([df_prices, df_melt], ignore_index=True)

        except Exception as e:
            print(f"Error for {ticker}: {e}")
    
    df_prices['Date'] = pd.to_datetime(df_prices['Date']).dt.strftime('%Y-%m-%d')

    print(df_prices)

    delete_query = "DELETE FROM StockData.spx.prices"

    with engine.connect() as connection:
        connection.execute(delete_query)
        print("Data deleted successfully")

    # Insert data into the database
    df_prices = df_prices.head(5000)
    chunk_size = 1000
    for i in tqdm(range(0, df_prices.shape[0], chunk_size)):
        chunk = df_prices[i:i+chunk_size]
        chunk.to_sql('prices', engine, schema='spx', if_exists='append', index=False)
    print("Data inserted successfully!")

    ##################################################################
    # Source quarterly fundamentals
    df_fundamentals = pd.DataFrame()

    # For now only first 10 tickers
    for ticker in tqdm(df_info['Symbol'].to_list()[:10]):
    # for ticker in tqdm(df_info['Symbol'].to_list()):
        try: 
            stock = yf.Ticker(ticker)
            df_temp = stock.quarterly_financials.transpose().reset_index()
            df_temp['Ticker'] = ticker
            
            df_melt = pd.melt(df_temp,
                             id_vars=['Ticker', 'index'])
            df_fundamentals = pd.concat([df_fundamentals, df_melt],
                                         ignore_index=True)
        except Exception as e:
            print(f"Error for {ticker}: {e}")

    df_fundamentals = df_fundamentals.rename(columns={'index': 'Date'})

    df_fundamentals['Date'] = pd.to_datetime(df_fundamentals['Date']).dt.strftime('%Y-%m-%d')

    print(df_fundamentals)

    delete_query = "DELETE FROM StockData.spx.financials"

    with engine.connect() as connection:
        connection.execute(delete_query)
        print("Data deleted successfully")

    # Insert data into the database
    df_fundamentals = df_fundamentals.head(2000)
    df_fundamentals.to_sql('financials', engine, schema='spx', if_exists='append', index=False)
    print("Data inserted successfully!")

except Exception as e:
    print("Error: ", e)
    exit(1)
