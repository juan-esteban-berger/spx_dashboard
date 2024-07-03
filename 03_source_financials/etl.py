import warnings
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import yfinance as yf
from tqdm import tqdm
from datetime import datetime

warnings.filterwarnings('ignore')

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

    # Source quarterly fundamentals
    df_fundamentals = pd.DataFrame()

    for ticker in tqdm(df_symbols['symbol'].tolist()):
        try:
            stock = yf.Ticker(ticker)
            df_temp = stock.quarterly_financials.transpose().reset_index()
            df_temp['Ticker'] = ticker

            df_melt = pd.melt(df_temp, id_vars=['Ticker', 'index'])
            df_fundamentals = pd.concat([df_fundamentals, df_melt], ignore_index=True)
        except Exception as e:
            print(f"Error for {ticker}: {e}")

    df_fundamentals = df_fundamentals.rename(columns={'index': 'Date'})

    df_fundamentals['Date'] = pd.to_datetime(df_fundamentals['Date']).dt.date

    # Output retrieved financials
    print(df_fundamentals)

    # Delete existing financials data
    cur.execute("DELETE FROM spx.financials")
    conn.commit()

    # Insert new financials data
    chunk_size = 1000
    for i in tqdm(range(0, len(df_fundamentals), chunk_size), desc="Inserting data"):
        chunk = df_fundamentals[i:i + chunk_size]
        execute_values(cur, "INSERT INTO spx.financials VALUES %s", chunk.to_records(index=False))
    print("Data inserted successfully!")
    conn.commit()

except Exception as e:
    print("Error: ", e)
    exit(1)

finally:
    if conn:
        conn.close()
