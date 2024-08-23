from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(dag_id="powerbi_dag",
         start_date=datetime(2024, 1, 22),
         schedule_interval="@daily") as dag:
    
    task1 = BashOperator(
        task_id="powerbi",
        bash_command='python.exe D:/HK7/ODAP/odap_process.py',
        dag=dag
    )

task1