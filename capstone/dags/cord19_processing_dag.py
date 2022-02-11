
import datetime

from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.redshift_to_s3_operator import RedshiftToS3Transfer
from airflow.providers.amazon.aws.transfers.redshift_to_s3 import RedshiftToS3Operator
from airflow.models import Variable


with DAG(
    dag_id="CORD19_PROCESSING",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')
    get_version = RedshiftSQLOperator(
        task_id='get_version',
        redshift_conn_id="redshift_db",
        sql="""
            select version();
        """,
    )
    drop_external_schema_if_exists = RedshiftSQLOperator(
        task_id='drop_schema',
        redshift_conn_id="redshift_db",
        sql="drop schema if exists "+ Variable.get('redshift_destination_external_schema_name') +" ;",
    )
    create_external_schema_pointing_to_datalake = RedshiftSQLOperator(
        task_id='create_external_schema_pointing_to_datalake',
        redshift_conn_id="redshift_db",
        sql=f"create external schema {Variable.get('redshift_destination_external_schema_name')} \
            from data catalog database  '{Variable.get('redshift_destination_glue_database_name')}' \
            iam_role '{Variable.get('redshift_role_arn')}' \
            create external database if not exists;",
    )
    drop_redshift_native_table_if_exists = RedshiftSQLOperator(
        task_id='drop_redshift_native_table_if_exists',
        redshift_conn_id="redshift_db",
        sql=f"drop table if exists public.{Variable.get('redshift_destination_table_name')};"
    )
    create_redshift_native_table = RedshiftSQLOperator(
        task_id='create_redshift_native_table',
        redshift_conn_id="redshift_db",
        sql=f"create table public.{Variable.get('redshift_destination_table_name')} \
            as select * from \
            {Variable.get('redshift_destination_external_schema_name')}.{Variable.get('redshift_destination_table_name')} ;"
    )
    unload_raw_data_to_s3 = RedshiftToS3Operator(
        task_id='unload_raw_data_to_s3',
        schema='public',
        table=Variable.get('redshift_destination_table_name'),
        s3_bucket=Variable.get('s3_staging_bucket'),
        s3_key="data/raw",
        redshift_conn_id='redshift_db',
        unload_options = ['CSV','parallel off', 'ALLOWOVERWRITE']
    )
    

    start >> get_version >> drop_external_schema_if_exists >> create_external_schema_pointing_to_datalake 
    create_external_schema_pointing_to_datalake >> drop_redshift_native_table_if_exists
    drop_redshift_native_table_if_exists >> create_redshift_native_table >> unload_raw_data_to_s3
    unload_raw_data_to_s3 >> end
