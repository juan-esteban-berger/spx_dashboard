import os
import psycopg2
from psycopg2.extras import execute_values
from data_fetcher import fetch_sp500_companies

host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
password = os.getenv('PGPASSWORD')
database = os.getenv('DATABASE')

try:
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=database)
    cur = conn.cursor()

    df_info = fetch_sp500_companies()

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
