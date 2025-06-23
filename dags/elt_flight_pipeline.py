from airflow import DAG
from airflow.decorators import task, task_group
from airflow.operators.python import PythonOperator
from elt_pipeline.task.extract import Extract
from elt_pipeline.task.load import Load
from elt_pipeline.task.transform import transform_group
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 5, 28),
}

@task_group(group_id="extract")
def extract_group():
    
    extract_aircrafts_data = PythonOperator(
        task_id="extract_aircrafts_data",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "aircrafts_data",
            "bucket_name": "extracted-data"
        }
    )

    extract_airports_data = PythonOperator(
        task_id="extract_airports_data",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "airports_data",
            "bucket_name": "extracted-data"
        }
    )

    extract_bookings = PythonOperator(
        task_id="extract_bookings",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "bookings",
            "bucket_name": "extracted-data"
        }
    )

    extract_boarding_passes = PythonOperator(
        task_id="extract_boarding_passes",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "boarding_passes",
            "bucket_name": "extracted-data"
        }
    )

    extract_seats = PythonOperator(
        task_id="extract_seats",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "seats",
            "bucket_name": "extracted-data"
        }
    )

    extract_flights = PythonOperator(
        task_id="extract_flights",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "flights",
            "bucket_name": "extracted-data"
        }
    )

    extract_ticket_flights = PythonOperator(
        task_id="extract_ticket_flights",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "ticket_flights",
            "bucket_name": "extracted-data"
        }
    )

    extract_tickets = PythonOperator(
        task_id="extract_tickets",
        python_callable=Extract.source_table,
        op_kwargs={
            "connection_id": "src_aircraft",
            "table_name": "tickets",
            "bucket_name": "extracted-data"
        }
    )

@task_group(group_id="load")
def load_group():
    load_aircrafts_data = PythonOperator(
        task_id="load_aircrafts_data",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "aircrafts_data",
            "connection_id": "dwh_aircraft"
        }
    )

    load_airports_data = PythonOperator(
        task_id="load_airports_data",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "airports_data",
            "connection_id": "dwh_aircraft"
        }
    )

    load_bookings = PythonOperator(
        task_id="load_bookings",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "bookings",
            "connection_id": "dwh_aircraft"
        }
    )

    load_tickets = PythonOperator(
        task_id="load_tickets",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "tickets",
            "connection_id": "dwh_aircraft"
        }
    )

    load_seats = PythonOperator(
        task_id="load_seats",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "seats",
            "connection_id": "dwh_aircraft"
        }
    )

    load_flights = PythonOperator(
        task_id="load_flights",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "flights",
            "connection_id": "dwh_aircraft"
        }
    )

    load_ticket_flights = PythonOperator(
        task_id="load_ticket_flights",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "ticket_flights",
            "connection_id": "dwh_aircraft"
        }
    )

    load_boarding_passes = PythonOperator(
        task_id="load_boarding_passes",
        python_callable=Load.bucket_to_staging,
        op_kwargs={
            "bucket_name": "extracted-data",
            "table_name": "boarding_passes",
            "connection_id": "dwh_aircraft"
        }
    )

    # Jika mau hubungkan satu sama lain secara berurutan:
    load_aircrafts_data >> load_airports_data >> load_bookings >> load_tickets >> \
    load_seats >> load_flights >> load_ticket_flights >> load_boarding_passes
    
with DAG(
    dag_id="etl_flight_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["flight"],
    max_active_tasks=1
) as dag:
    extract_group()  >> load_group() >> transform_group() # memanggil task group




