
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

from tqdm import tqdm
from langdetect import detect
from langdetect import DetectorFactory
from pprint import pprint
DetectorFactory.seed = 3


def verify_data():
    
    print(f'::::::: PRIOR ')
    print(f'::::::: AFTER ')
    return True

