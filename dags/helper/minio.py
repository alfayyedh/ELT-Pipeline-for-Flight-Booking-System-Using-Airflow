from airflow.hooks.base import BaseHook
from minio import Minio
from io import BytesIO
import logging


class MinioClient:
    @staticmethod
    def _get():
        try:
            minio = BaseHook.get_connection('minio')
            client = Minio(
                endpoint=minio.extra_dejson['endpoint_url'],
                access_key=minio.login,
                secret_key=minio.password,
                secure=False
            )

            client.list_buckets()
            logging.info(f"Successfully connected to MinIO")
                         
            return client
        
        except Exception as e:
            logging.error(f"Failed to connect to MinIO: {e}", exc_info=True)
            raise
