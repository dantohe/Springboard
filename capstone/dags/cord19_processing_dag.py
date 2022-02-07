from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator


from cord19_load_data_into_redshift_operator import LoadDataIntoRedshiftOperator

default_args = {
    'owner': 'dantohe',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3),
    'catchup': False,
    'start_date': datetime(2021, 1, 1)
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    'cord19_ml_processor_dag',
    default_args=default_args,
    description='Creates an ML pipeline for processing the CORD19 corpus',
    schedule_interval='@once',
    max_active_runs=1)

# STEP 0: START ==========================================================
start_operator = DummyOperator(
    task_id='begin_execution', 
    dag=dag)
# ========================================================================

# STEP 1: STAGE IN REDSHIFT ==============================================
load_data_into_redshift_operator = LoadDataIntoRedshiftOperator(
    
    task_id='load_cord19_data_into_redshif',
    redshift_destination_conn_id='redshift_dw',
    redshift_destination_db=Variable.get('redshift_db'),
    redshift_destination_table_name=Variable.get('redshift_destination_table_name'),
    redshift_destination_external_schema_name=Variable.get('redshift_destination_external_schema_name'),
    redshift_destination_glue_database_name=Variable.get('redshift_destination_glue_database_name'),
    iam_role=Variable.get('redshift_role_arn'),
    region=Variable.get('my_region'),
    dag=dag)

# ========================================================================

# ========================================================================

# STEP N: END ============================================================

end_operator = DummyOperator(
    task_id='stop_execution',
    dag=dag)

# ========================================================================

start_operator >> load_data_into_redshift_operator
load_data_into_redshift_operator >> end_operator