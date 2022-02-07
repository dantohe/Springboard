import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy import DummyOperator
from airflow.models.connection import Connection

# create_pet_table, populate_pet_table, get_all_pets, and get_birth_date are examples of tasks created by
# instantiating the Postgres Operator

c = Connection( conn_id="red", conn_type="postgres", description="connection description", host="3.139.214.8", login="redshift",password="kljhdfsKLJDD12345",)


with DAG(
    dag_id="cord19_processing_02",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
) as dag:
    start = DummyOperator(task_id='begin_execution')
    end = DummyOperator(task_id='end_execution')
    get_redshift_version = PostgresOperator(
        task_id="get_redshift_version",
        postgres_conn_id="red",
        sql="""
            select version();
            """,
    )
#     get_all_pets = PostgresOperator(task_id="get_all_pets", sql="SELECT * FROM pet;")
#     get_birth_date = PostgresOperator(
#         task_id="get_birth_date",
#         sql="""
#             SELECT * FROM pet
#             WHERE birth_date
#             BETWEEN SYMMETRIC DATE '{{ params.begin_date }}' AND DATE '{{ params.end_date }}';
#             """,
#         params={'begin_date': '2020-01-01', 'end_date': '2020-12-31'},
#     )

    start >> get_redshift_version >> end