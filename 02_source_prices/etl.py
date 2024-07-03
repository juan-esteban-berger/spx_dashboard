import warnings
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import yfinance as yf
from tqdm import tqdm
from datetime import datetime, timedelta

host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
password = os.getenv('PGPASSWORD')
database = os.getenv('DATABASE')

try:
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=database)
    cur = conn.cursor()

    # Get symbols from the spx.info table
    cur.execute("SELECT symbol FROM spx.info")
    df_symbols = pd.DataFrame(cur.fetchall(), columns=['symbol'])

    # Source prices
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=10*365)

    df_prices = pd.DataFrame()

    for ticker in tqdm(df_symbols['symbol'].tolist()):
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

    # Format date
    df_prices['Date'] = pd.to_datetime(df_prices['Date']).dt.date

    # Output retrieved prices
    print(df_prices)

    # Delete existing price data
    cur.execute("DELETE FROM spx.prices")
    conn.commit()
    print("Data deleted successfully!")

    # Insert new price data
    chunk_size = 1000
    for i in tqdm(range(0, len(df_prices), chunk_size), desc="Inserting data"):
        chunk = df_prices[i:i + chunk_size]
        execute_values(cur, "INSERT INTO spx.prices VALUES %s", chunk.to_records(index=False))
    conn.commit()
    print("Data inserted successfully!")

except Exception as e:
    print("Error: ", e)
    exit(1)

finally:
    if conn:
        conn.close()
