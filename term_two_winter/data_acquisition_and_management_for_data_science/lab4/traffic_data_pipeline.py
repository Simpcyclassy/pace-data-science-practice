from datetime import datetime, timedelta

from utils.combine_extracted_files import combine_extracted_files
from utils.create_directories import create_directories
# Remove the Python download function since we're using the Bash script now
# from utils.download_data import download_traffic_data
from utils.extract_payment_data import extract_payment_data
from utils.extract_tollplaza_data import extract_tollplaza_data
from utils.extract_traffic_data import extract_traffic_data
from utils.extract_vehicle_data import extract_vehicle_data
from utils.transform_combined_data import transform_combined_data

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator  # Airflow 2.x

# Default DAG arguments
default_args = {
    'owner': 'chioma',
    'depends_on_past': False,
    'email': 'chioma.onyekpere@gmail.com',
    'start_date': datetime(2025, 2, 17),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    dag_id='traffic_data_pipeline',
    default_args=default_args,
    description='A DAG for processing traffic data with ETL steps',
    schedule_interval='@daily',
    catchup=False
)

# **Task 1: Create Directories**
create_dirs_task = PythonOperator(
    task_id='create_directories',
    python_callable=create_directories,
    dag=dag
)

# **Task 2: Download Traffic Data using BashOperator**
download_traffic_data_task = BashOperator(
    task_id='download_traffic_data',
    bash_command='bash /Users/chiomaonyekpere/airflow/scripts/download_traffic_data.sh',
    dag=dag,
    execution_timeout=timedelta(minutes=10)
)
download_traffic_data_task.template_ext = []

# **Task 3: Extract Traffic Data**
extract_traffic_data_task = PythonOperator(
    task_id='extract_traffic_data',
    python_callable=extract_traffic_data,
    dag=dag
)

# **Tasks 4-6: Extract Vehicle, Toll Plaza, and Payment Data (Parallel Execution)**
extract_vehicle_data_task = PythonOperator(
    task_id='extract_vehicle_data',
    python_callable=extract_vehicle_data,
    dag=dag
)

extract_tollplaza_task = PythonOperator(
    task_id='extract_tollplaza_data',
    python_callable=extract_tollplaza_data,
    dag=dag
)

extract_payment_data_task = PythonOperator(
    task_id='extract_payment_data',
    python_callable=extract_payment_data,
    dag=dag
)

# **Task 7: Combine Extracted Files**
combine_files_task = PythonOperator(
    task_id='combine_extracted_files',
    python_callable=combine_extracted_files,
    dag=dag
)

# **Task 8: Transform Combined Data**
transform_combined_data_task = PythonOperator(
    task_id='transform_combined_data',
    python_callable=transform_combined_data,
    dag=dag
)

# **Define Pipeline Execution Order**
# Step 1: Create directories
create_dirs_task >> download_traffic_data_task >> extract_traffic_data_task  

# Step 2: Extract data in parallel (Tasks 4, 5, 6)
extract_traffic_data_task >> [extract_vehicle_data_task, extract_tollplaza_task, extract_payment_data_task]  

# Step 3: Combine extracted files (Task 7)
[extract_vehicle_data_task, extract_tollplaza_task, extract_payment_data_task] >> combine_files_task  

# Step 4: Transform data (Task 8)
combine_files_task >> transform_combined_data_task
