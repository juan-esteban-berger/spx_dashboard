import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
from .data_fetcher import fetch_quarterly_financials

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

    # Fetch quarterly financials
    df_fundamentals = fetch_quarterly_financials(df_symbols['symbol'].tolist())

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
