from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
from io import StringIO

BASE_PATH = "/opt/airflow/dags"

class Execute:
    @staticmethod
    def _execute_query(connection_id, query):
        hook = PostgresHook(postgres_conn_id=connection_id)
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def insert_dataframe_direct(connection_id, table_name, dataframe):
        pg_hook = PostgresHook(postgres_conn_id=connection_id)
        engine = pg_hook.get_sqlalchemy_engine()

        dataframe.to_sql(
            name=table_name,
            con=engine,
            schema='stg',         
            if_exists='append',     
            index=False
        )

    @staticmethod
    def extract_table_to_csv(connection_id: str, table_name: str) -> str:
        hook = PostgresHook(postgres_conn_id=connection_id)
        engine = hook.get_sqlalchemy_engine()
        
        df = pd.read_sql_table(table_name, con=engine, schema='bookings')
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        return csv_buffer.getvalue()