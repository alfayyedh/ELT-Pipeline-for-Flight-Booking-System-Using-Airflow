# ELT-Pipeline-for-Flight-Booking-System-Using-Airflow
An automated data pipeline that extracts data from a source database, stores it temporarily in an object store, and loads it into a data warehouse. The pipeline will be orchestrated using Apache Airflow.

## System Architecture and Tasks
![image](https://github.com/user-attachments/assets/2882655b-e3a5-4eb7-bde3-8097382ae879)

1. Data Extraction 
   - Extract selected tables from the source database on a daily basis (optionally incrementally).
2. Data  Loading
   - Load the extracted data to MinIO (object store) in CSV format.
3. Data Transformation
   - Transform the staging data into dimensional and fact tables using SQL scripts.
4. Workflow Orchestration
   - Orchestrate all of the above using Airflow DAG with well-structured TaskGroups
  
## Project Structure

```
├── aircraft_db/
│   └── init.sql                  # SQL script to initialize source database
├── aircraft_dwh/
│   ├── init.sql                  # SQL script to initialize data warehouse
│   └── stg_schema.sql            # SQL schema for staging tables
├── dags/
│   ├── elt_flight_pipeline.py    # Main Airflow DAG
│   └── task/
│       ├── extract.py            # Extract tasks
│       ├── load.py               # Load tasks
│       └── transform.py          # Transform tasks
├── helper/
│   ├── __init__.py               # Package initializer
│   ├── minio.py                  # MinIO connection helper
│   └── postgres.py               # PostgreSQL connection helper
├── include/
│   └── sql/
│       └── transform/            # SQL transform scripts
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Dockerfile for custom image build
├── fernet.py                     # Airflow Fernet key
├── requirements.txt              # Python dependencies
└── start.sh                      # Shell script to start project

```
## How To Run
### 1. Clone the repository
```
git clone https://github.com/yourusername/elt-flight-booking.git
cd elt-flight-booking
```

### 2. Copy the Data Source
```
- You need to copy the Data Souce from this link https://drive.google.com/file/d/1Zu5grD6mKuCcLagggE9R8ILjzvPIbXDQ/view?usp=sharing
- You'll need to store it as aircraft_db/init.sql
```

### 3. Generate Fernet Key
This key encrypts credentials in Airflow connections.
```
pip install cryptography==45.0.2
python3 fernet.py
```
Copy the output and place it on `.env` file

### 4. Create `.env` file

```
# Fernet key for encrypting Airflow connections (generate using fernet.py script)
AIRFLOW_FERNET_KEY=...

# Airflow metadata database connection URI
AIRFLOW_DB_URI=postgresql+psycopg2://airflow:airflow@airflow_metadata/airflow

# Airflow DB configuration
AIRFLOW_DB_USER=...
AIRFLOW_DB_PASSWORD=...
AIRFLOW_DB_NAME=...

# Warehouse database configuration
DWH_DB_USER=...
DWH_DB_PASSWORD=...
DWH_DB_NAME=...

# Source database configuration
SOURCE_DB_USER=...
SOURCE_DB_PASSWORD=...
SOURCE_DB_NAME=...

# MinIO configuration
MINIO_ROOT_USER=...
MINIO_ROOT_PASSWORD=...
```

### 5. Build and Start Service
```
docker-compose up --build -d
```

### 6. Create Airflow User
```
docker exec -it airflow_standalones airflow users create \
    --username your_username \
    --firstname First \
    --lastname Last \
    --role Admin \
    --email your@email.com \
    --password your_password
```

### 7. Open Airflow UI
Access the UI at: http://localhost:8080 (or another defined port).

## Setup Airflow Connections
3 necessary connections:
- PostgreSQL - Source Database
- PostgreSQL - Data Warehouse
- MinIO - Object Storage

Steps :
Go to Admin > Connections
Click + to add new connection
Fill in the details based on your .env setup

## Run Airflow DAG
After accessing the airflow UI you'll need to:
1. Select the the DAG named `elt_flight_pipeline`
2. Find the play button then click to start DAG
3. Monitor the task progress in task view or tree view

## Result
- Extracted source data on MinIO bucket.
  Data will be store at folder named `extracted-data` as CSV format.
  ![image](https://github.com/user-attachments/assets/578174ed-fe05-4db0-9e62-9c411756bfd6)

- Staging dan Transformed Data
  - To verify the staging dan transform data, you should connect to your preferred database client.
  - You'll see :
     - Staging data on `stg` schema
     - Transformed data on `final` schema

## DAG Result
![image](https://github.com/user-attachments/assets/5636ebed-4387-48c3-808b-e62303706f51)
- Extract task running in parallel
- Load task running sequentially
- Transform task running sequentially














