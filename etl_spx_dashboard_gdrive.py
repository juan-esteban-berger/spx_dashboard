import os
import json
import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import re

creds_path = "/home/juaneshberger/Credentials/gdrive_credentials.json"
with open(creds_path, 'r') as file:
    creds_data = json.load(file)

JSON_CREDS = json.dumps(creds_data)
sheets_creds_path="/home/juaneshberger/Credentials/spx_sheets.toml"
with open(sheets_creds_path, 'r') as f:
    lines=f.read()

SPX_INFO_GDRIVE = re.search(r"info_gdrive\s*=\s*\'(.+?)\'", lines).group(1)
SPX_PRICES_GDRIVE = re.search(r"prices_gdrive\s*=\s*\'(.+?)\'", lines).group(1)
SPX_FINANCIALS_GDRIVE = re.search(r"financials_gdrive\s*=\s*\'(.+?)\'", lines).group(1)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2024, 5, 27, tz="America/Guatemala"),
    'retries': 2,
    'retry_delay': timedelta(hours=2),
}

dag = DAG(
    'etl_spx_dashboard_gdrive',
    default_args=default_args,
    schedule_interval='45 20 * * *',
    catchup=False,
    tags=['spx_dashboard'],
)

tasks = {
    'source_info_gdrive': 'spx_11_source_info_gdrive',
    'source_prices_gdrive': 'spx_12_source_prices_gdrive',
    'source_financials_gdrive': 'spx_13_source_financials_gdrive'
}

task_operators = []

for task_id, image in tasks.items():
    run_task = DockerOperator(
        task_id=task_id,
        image=image,
        network_mode='host',
        environment={
            'JSON_CREDS': JSON_CREDS,
            'SPX_INFO_GDRIVE': SPX_INFO_GDRIVE,
            'SPX_PRICES_GDRIVE': SPX_PRICES_GDRIVE,
            'SPX_FINANCIALS_GDRIVE': SPX_FINANCIALS_GDRIVE,
        },
        execution_timeout=timedelta(hours=4),
        auto_remove=True,
        dag=dag,
    )
    task_operators.append(run_task)

for i in range(len(task_operators) - 1):
    task_operators[i] >> task_operators[i + 1]
