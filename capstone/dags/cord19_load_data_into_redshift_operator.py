from airflow.hooks.postgres_hook import PostgresHook
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults



class LoadDataIntoRedshiftOperator(BaseOperator):
    """
    Loads data into Redshift.
    """

    @apply_defaults
    def __init__(
            self,
            redshift_destination_conn_id: str,
            redshift_destination_db: str,
            redshift_destination_table_name: str,
            redshift_destination_external_schema_name: str,
            redshift_destination_glue_database_name: str,
            iam_role: str,
            region: str,
            *args, **kwargs) -> None:

        super(LoadDataIntoRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_destination_conn_id = redshift_destination_conn_id
        self.redshift_destination_db = redshift_destination_db
        self.redshift_destination_table_name = redshift_destination_table_name
        self.redshift_destination_external_schema_name = redshift_destination_external_schema_name
        self.redshift_destination_glue_database_name = redshift_destination_glue_database_name
        self.iam_role = iam_role
        self.region = region

    def execute(self, context):
        """
        Prepare the SQL statement, replacing variables and run the command.

        Parameters
        ----------
        context {object} Airflow context
        """
        print(f"EXECUTING")
        hook = self.prepare_hook()
        sql = self.prepare_sql()
        hook.run(sql, autocommit=True)
        for output in hook.conn.notices:
            self.log.info(output)

    def prepare_hook(self):
        """
        Returns the postgres hook, based on the configuration passed into the operator.
        """
        return PostgresHook(
            postgres_conn_id=self.redshift_destination_conn_id,
            schema=self.redshift_destination_db)

    def prepare_sql(self):
        """
        Prepares the SQL statement using the parameters provided to the Operator.
        """
        sql = []

        
#         create external schema {redshift_destination_external_schema_name} from data catalog
#          database '{redshift_destination_glue_database_name}'
#          iam_role '{redshift_role_arn}'
#          create external database if not exists;		

#         sql.append(f'drop schema if exists {self.redshift_destination_external_schema_name};')            
#         sql.append(f"create external schema {self.redshift_destination_external_schema_name} from data catalog\
#                      database '{redshift_destination_glue_database_name}' \
#                      iam_role '{redshift_role_arn}' \
#                      create external database if not exists; ")
        sql.append('select version();')

        return '\n'.join(sql)
