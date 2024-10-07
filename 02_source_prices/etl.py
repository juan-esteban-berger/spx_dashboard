import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
from .data_fetcher import fetch_stock_prices

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

    # Fetch stock prices
    df_prices = fetch_stock_prices(df_symbols['symbol'].tolist())

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
