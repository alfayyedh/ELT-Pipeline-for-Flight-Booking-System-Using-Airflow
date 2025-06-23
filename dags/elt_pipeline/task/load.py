from helper.minio import MinioClient
from helper.postgres import Execute
from io import BytesIO
import pandas as pd
import json

class Load:
    @staticmethod
    def bucket_to_staging(bucket_name: str, table_name: str, connection_id: str):
        """
        Load a CSV file from a MinIO bucket and insert its content into a staging table.

        This method:
        1. Retrieves the CSV file from the specified MinIO bucket.
        2. Reads the CSV content into a pandas DataFrame.
        3. Converts specific JSON-like columns to JSON strings.
        4. Truncates the target staging table.
        5. Inserts the DataFrame data into the staging table.

        Parameters
        ----------
        bucket_name : str
            The name of the MinIO bucket containing the CSV file.
        table_name : str
            The name of the staging table where data will be inserted.
        connection_id : str
            Airflow connection ID for the target database.

        Returns
        -------
        None
        """

        minio_client = MinioClient._get()

        object_name = f"temp/{table_name}.csv"
        response = minio_client.get_object(bucket_name, object_name)
        csv_data = response.read()

        df = pd.read_csv(BytesIO(csv_data))

        # List of JSON like columns
        jsonb_columns = ['model', 'airport_name', 'city', 'contact_data']

        # Convert specific JSON-like columns to JSON strings
        for column_name in jsonb_columns:
                if column_name in df.columns:
                    # Convert each row's dictionary/list to a JSON-formatted string
                    df[column_name] = df[column_name].apply(json.dumps)
                    print(df[column_name].iloc[0], type(df[column_name].iloc[0]))

        # Truncate (optional)
        Execute._execute_query(
            connection_id=connection_id,
            query=f"TRUNCATE TABLE stg.{table_name} CASCADE;"
        )

        # Insert dataframe into staging schema
        Execute.insert_dataframe_direct(
            connection_id=connection_id,
            table_name=table_name, 
            dataframe=df
        )
