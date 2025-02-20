import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': '2023-06-05',
    'email': 'chioma.onyekpere@gmail.com',
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    dag_id='hello-world',
    schedule_interval='@daily',
    default_args=default_args,
    description='Airflow Team Project'
)

# Task to get the current directory
current_dir = BashOperator(
    task_id='current_dir',
    bash_command='pwd',
    dag=dag
)

# Task to list files in the directory
get_list = BashOperator(
    task_id='get_list',
    bash_command='ls -la',
    dag=dag
)

# Define task dependencies
current_dir >> get_list
