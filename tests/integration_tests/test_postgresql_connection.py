import pytest
import psycopg2
import json

def test_postgresql_connection():
    # Load PostgreSQL credentials
    with open("/home/juaneshberger/Credentials/pgcreds.json", "r") as f:
        pg_creds = json.load(f)

    try:
        conn = psycopg2.connect(
            host=pg_creds['host'],
            port=pg_creds['port'],
            user=pg_creds['user'],
            password=pg_creds['password'],
            database=pg_creds['database']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1
        cursor.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to PostgreSQL: {str(e)}")
