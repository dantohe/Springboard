
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

dt = datetime.datetime.today()
s3 = boto3.resource('s3')

# 
# 
def load_raw_data_from_s3_and_save_it_locally():
#     bucket, filename = "dantohe-my-experimental-iac-02", "data/raw/2/12/2022/alleninstitute_metadata_000"
    obj = s3.Object(Variable.get('s3_staging_bucket'), Variable.get('unload_raw_data_to_s3_key')+'/'+Variable.get('unload_raw_data_to_s3_filename'))
    with BytesIO(obj.get()['Body'].read()) as bio:
        df = pd.read_csv(bio)
    print(f':::::::dataframe:\n{df.info()}')
    df.to_csv(Variable.get('raw_data_file'))
    print(f':::::::Dataframe was saved locally')
    return True


