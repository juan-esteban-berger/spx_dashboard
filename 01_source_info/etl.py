import warnings

import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values

host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
password = os.getenv('PGPASSWORD')
database = os.getenv('DATABASE')

try:
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=database)
    cur = conn.cursor()

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    df_info = pd.read_html(url)[0]
    df_info['Date added'] = pd.to_datetime(df_info['Date added']).dt.date

    df_info.columns = ['symbol', 'security', 'gics_sector', 'gics_sub_industry', 'headquarters_location', 'date_added', 'cik', 'founded']

    df_info['founded'] = df_info['founded'].str.extract(r'(\d+)')

    df_info['cik'] = df_info['cik'].astype(str)

    cur.execute("DELETE FROM spx.info")
    conn.commit()

    execute_values(cur, "INSERT INTO spx.info VALUES %s", df_info.to_records(index=False))
    print("Replacing data in spx.info")
    conn.commit()
    print("Data loaded successfully")

except Exception as e:
    print("Error: ", e)
    exit(1)

finally:
    if conn:
        conn.close()
