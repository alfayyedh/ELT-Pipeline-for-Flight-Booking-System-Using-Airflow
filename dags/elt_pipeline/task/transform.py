from airflow.decorators import task_group
from airflow.providers.postgres.operators.postgres import PostgresOperator

@task_group(group_id="transform")
def transform_group():
    transform_dim_aircrafts = PostgresOperator(
        task_id="transform_dim_aircrafts",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/dim_aircrafts.sql"
    )

    transform_dim_airport = PostgresOperator(
        task_id="transform_dim_airport",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/dim_airport.sql"
    )

    transform_dim_passenger = PostgresOperator(
        task_id="transform_dim_passenger",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/dim_passenger.sql"
    )

    transform_dim_seat = PostgresOperator(
        task_id="transform_dim_seat",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/dim_seat.sql"
    )

    transform_fct_boarding_pass = PostgresOperator(
        task_id="transform_fct_boarding_pass",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/fct_boarding_pass.sql"
    )

    transform_fct_booking_ticket = PostgresOperator(
        task_id="transform_fct_booking_ticket",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/fct_booking_ticket.sql"
    )

    transform_fct_flight_activity = PostgresOperator(
        task_id="transform_fct_flight_activity",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/fct_flight_activity.sql"
    )

    transform_fct_seat_occupied_daily = PostgresOperator(
        task_id="transform_fct_seat_occupied_daily",
        postgres_conn_id="dwh_aircraft",
        sql="include/sql/transform/fct_seat_occupied_daily.sql"
    )

    transform_dim_aircrafts >> transform_dim_airport >> transform_dim_passenger >> transform_dim_seat >> \
    transform_fct_boarding_pass >> transform_fct_booking_ticket >> transform_fct_flight_activity >> transform_fct_seat_occupied_daily