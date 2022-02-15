
import datetime
import pandas as pd
import io
import os
import boto3
from io import BytesIO

from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.redshift_to_s3_operator import RedshiftToS3Transfer
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.transfers.redshift_to_s3 import RedshiftToS3Operator
from airflow.models import Variable


from transfer_utils import *
from cleanup_utils import *
from language_utils import *
from spacy_utils import *
from ml_utils_vectorization import *


dt = datetime.datetime.today()
s3 = boto3.resource('s3')

# 
# 
# 
# 
# DAG works
# 
# 
# 

with DAG(
    dag_id="CORD19_MACHINE_LEARNING",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval=None,
    catchup=False,
    tags=['ML-engineering'],
) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')
    
    load_preprocessed_data_from_s3_and_save_it_locally = PythonOperator(
        task_id='load_preprocessed_data_from_s3_and_save_it_locally',  python_callable=load_preprocessed_data_from_s3_and_save_it_locally
    )
    
    verify_data = PythonOperator(
        task_id='verify_data',  python_callable=verify_data
    )
    
#     put_spacy_preprocessed_data_into_s3 = PythonOperator(
#         task_id='put_spacy_preprocessed_data_into_s3',  python_callable=put_spacy_preprocessed_data_into_s3
#     )
    
    

    start >> load_preprocessed_data_from_s3_and_save_it_locally >> verify_data >> end
