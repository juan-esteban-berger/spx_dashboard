import os
import json
import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

pg_creds_path = "/home/juaneshberger/Credentials/pgcreds.json"

with open(pg_creds_path, 'r') as file:
    pg_data = json.load(file)

PG_HOST = pg_data['host']
PG_PORT = pg_data['port']
PG_USER = pg_data['user']
PGPASSWORD = pg_data['password']
PG_DATABASE = pg_data['database']

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2024, 5, 27, tz="America/Guatemala"),
    'retries': 2,
    'retry_delay': timedelta(hours=2),
}

dag = DAG(
    'etl_spx_dashboard',
    default_args=default_args,
    schedule_interval='0 20 * * *',
    catchup=False,
    tags=['spx_dashboard'],
)

tasks = {
    'source_info': 'spx_01_source_info',
    'source_prices': 'spx_02_source_prices',
        'source_financials': 'spx_03_source_financials'
}

task_operators = []

for task_id, image in tasks.items():
    run_task = DockerOperator(
        task_id=task_id,
        image=image,
        network_mode='host',
        environment={
            'HOST': PG_HOST,
            'PORT': PG_PORT,
            'USER': PG_USER,
            'PGPASSWORD': PGPASSWORD,
            'DATABASE': PG_DATABASE
        },
        execution_timeout=timedelta(hours=4),
        auto_remove=True,
        dag=dag,
    )
    task_operators.append(run_task)

for i in range(len(task_operators) - 1):
    task_operators[i] >> task_operators[i + 1]
