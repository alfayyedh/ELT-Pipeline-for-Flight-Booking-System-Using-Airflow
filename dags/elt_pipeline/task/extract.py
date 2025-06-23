from airflow.providers.postgres.hooks.postgres import PostgresHook
from helper.minio import MinioClient
from helper.postgres import Execute
from io import BytesIO
import logging

class Extract:

    @staticmethod
    def source_table(connection_id: str, table_name: str, bucket_name: str):
        """
        Extracts data from a database table and uploads it as a CSV file to a MinIO bucket.

        This function:
        1. Extracts the specified table to a CSV format.
        2. Connects to the MinIO server.
        3. Creates the target bucket if it does not exist.
        4. Uploads the CSV file to the bucket under the 'temp/' folder.

        Parameters:
        ----------
        connection_id : str
            The Airflow connection ID for the source database.
        table_name : str
            The name of the table to extract.
        bucket_name : str
            The name of the MinIO bucket to upload the CSV file to.

        Returns:
        -------
        None
        """

        # Extract table to CSV string
        csv_content = Execute.extract_table_to_csv(connection_id=connection_id, table_name=table_name)

        # Connection to MinIO
        minio_client = MinioClient._get()

        # Create bucket if not yet exist
        if not minio_client.bucket_exists(bucket_name):
            logging.info(f"Bucket '{bucket_name}' is not exist. Creating...")
            minio_client.make_bucket(bucket_name)
        else:
            logging.info(f"Bucket '{bucket_name}' is exist.")

        # Upload file to MinIO
        csv_bytes = csv_content.encode('utf-8')
        csv_buffer = BytesIO(csv_bytes)

        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=f"temp/{table_name}.csv",
            data=csv_buffer,
            length=len(csv_bytes),
            content_type="application/csv"
        )
