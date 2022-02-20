
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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

dt = datetime.datetime.today()
s3 = boto3.resource('s3')

from tqdm import tqdm
from langdetect import detect
from langdetect import DetectorFactory
from pprint import pprint
DetectorFactory.seed = 3


def verify_data():
    dataframe = pd.read_csv(Variable.get('spacy_preprocessed'))
    print(f'::::::: PRIOR \n type {type(dataframe)} ')
    print(f'::::::: shape {dataframe.shape}')
    print(f'::::::: info {dataframe.info()}')
    print(f'::::::: AFTER ')
    dataframe.to_csv(Variable.get('spacy_preprocessed'))
    return True


"""
"""
def collect_small_subset():
    dataframe = pd.read_csv(Variable.get('spacy_preprocessed'))
    print(f'::::::: PRIOR \n type {type(dataframe)} \n shape {dataframe.shape} \n info {dataframe.info()}')
    journals = ['PLoS One','bioRxiv','Virology','Viruses','The Journal of general virology']
    dataframe_filtered = dataframe[(dataframe['publish_time']>'2020-01-01') & (dataframe['journal'].isin(journals))]
    
    print(f'::::::: AFTER ')
    dataframe_filtered.to_csv(Variable.get('ml_cord19_small_subset'))
    return True



def compute_sparse_matrix(input):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(input.astype('U'))

def compute_sparse_matrix_with_max(input, max_features):
    vectorizer = TfidfVectorizer(max_features=max_features)
    return vectorizer.fit_transform(input.astype('U'), max_features)


def vectorization_compute_sparse_matrix():
    dataframe = pd.read_csv(Variable.get('ml_cord19_small_subset'))
    print(f'::::::: PRIOR \n type {type(dataframe)} \n shape {dataframe.shape} \n info {dataframe.info()}')
    tfidf_matrix = compute_sparse_matrix(dataframe['abstract_processed'].values)
    print(f':::::::The matrix {type(tfidf_matrix)} size: {tfidf_matrix}')
    print(f'::::::: AFTER ')
#     dataframe.to_csv(Variable.get('ml_cord19_small_subset'))
    return True

def vectorization_compute_sparse_matrix():
    dataframe = pd.read_csv(Variable.get('ml_cord19_small_subset'))
    print(f'::::::: PRIOR \n type {type(dataframe)} \n shape {dataframe.shape} \n info {dataframe.info()}')
    unique_number_of_tokens = dataframe['abstract_processed'].nunique() 
    tfidf_matrix_with_max = compute_sparse_matrix_with_max(dataframe['abstract_processed'].values, unique_number_of_tokens)
#     tfidf_matrix = compute_sparse_matrix(dataframe['abstract_processed'].values)
    print(f':::::::The matrix {type(tfidf_matrix_with_max)} size: {tfidf_matrix_with_max}')
    print(f'::::::: AFTER ')
#     TODO: save matrix to disk
#     dataframe.to_csv(Variable.get('ml_cord19_small_subset'))
    return True


def vectorization_reduce_dimensionality_with_PCA():
    dataframe = pd.read_csv(Variable.get('ml_cord19_small_subset'))
    print(f'::::::: PRIOR \n type {type(dataframe)} \n shape {dataframe.shape} \n info {dataframe.info()}')
    unique_number_of_tokens = dataframe['abstract_processed'].nunique() 
    tfidf_matrix_with_max = compute_sparse_matrix_with_max(dataframe['abstract_processed'].values, unique_number_of_tokens)
#     tfidf_matrix = compute_sparse_matrix(dataframe['abstract_processed'].values)
    pca = PCA(n_components=0.95, random_state=3)
    tfidf_matrix_pcaed= pca.fit_transform(tfidf_matrix_with_max.toarray())
    print(f':::::::The matrix {type(tfidf_matrix_pcaed)} size: {tfidf_matrix_pcaed} \n {tfidf_matrix_pcaed.shape}')
    print(f'::::::: AFTER ')
#     TODO: save matrix to disk
#     dataframe.to_csv(Variable.get('ml_cord19_small_subset'))
    return True