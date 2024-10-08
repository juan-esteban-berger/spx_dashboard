import subprocess
import pytest

def test_etl_spx_dashboard_gdrive_e2e():
    dag_id = 'etl_spx_dashboard_gdrive'
    command = f"airflow dags trigger {dag_id}"
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"DAG {dag_id} triggered successfully")
        print(f"Output: {result.stdout}")
    else:
        pytest.fail(f"Failed to trigger DAG {dag_id}. Error: {result.stderr}")

if __name__ == "__main__":
    pytest.main([__file__])
