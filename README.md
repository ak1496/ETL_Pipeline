# Data Processing Pipeline with Airflow, Spark, MySQL, PostgreSQL & Superset
## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Steps for execution](Steps for execution)


## Project Overview
This project sets up a robust data processing pipeline using Docker Compose, orchestrating data flow from raw CSV files through MySQL and PySpark for transformation, loading into PostgreSQL, and finally visualizing insights with Apache Superset. Apache Airflow manages the entire workflow, ensuring reliable and scheduled execution of ETL tasks.

## Features
- **Data Ingestion:** Automated loading of CSV data into a MySQL staging database.
- **Data Transformation:** Leveraging PySpark for complex data cleaning, aggregation, and transformation.
- **Data Warehousing:** Storing processed data in a PostgreSQL database optimized for analytics.
- **Workflow Orchestration:** Apache Airflow for scheduling, monitoring, and managing ETL workflows.
- **Data Visualization:** Apache Superset for creating interactive dashboards and exploring data.
- **Containerized Environment:** All services run in Docker containers for easy setup and reproducibility.
- **Version Control for BI Assets:** Mechanism to export and import Superset dashboards for Git versioning.

## Architecture
The pipeline follows a typical Extract, Transform, Load (ETL) pattern:
1.  **Extract (E):** Raw data (e.g., CSV files) is read from the `data/raw_data` directory.
2.  **Load (L) to Staging:** Ingested into a MySQL database for temporary storage and initial cleansing.
3.  **Transform (T):** Data from MySQL is processed using PySpark for transformations (e.g., aggregation, joins).
4.  **Load (L) to Reporting:** Transformed data is loaded into a PostgreSQL database, serving as the analytical data store.
5.  **Visualization:** Apache Superset connects to the PostgreSQL database to build interactive dashboards and reports.
6.  **Orchestration:** Apache Airflow automates and schedules all these steps.

## CSV Raw Data (data/raw_data)   -----> MySQL DB (Staging) ----->  PySpark (Transform) ----->  PostgreSQL (Loading for Reporting)  ----->  Superset (Reporting) 

## Prerequisites
Before you begin, ensure you have the following installed on your system:
-   **Git**: For cloning the repository.
-   **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose).
-   **Docker Compose**: Usually included with Docker Desktop.



### Steps for execution

    step-1
        Clone the repository
        command: git clone <your_repo_url>
    
    Step-2
        Change the directory and build the services
        command: cd ETL_Pipeline
        command: docker-compose up -d --build
        
        Note:
            In case of error(✘ Container etl_pipeline-airflow-webserver-1  Error), you see the logs using 
            command: docker-compose logs airflow-webserver. 
            
            If it is permission issue(PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/scheduler') give permission to logs folder
            command: sudo chmod -R 777 logs/
            
    Step-3
        
         Go to airflow UI http://localhost:8080/ (username: airflow, passowd: airflow). Trigger a run.
         veriy data and schema:
            mysql
             docker-compose exec -it mysql_db mysql -u mysql_user -p
             show tables;
             use raw_data_db;
             show tables;
             select * from raw_csv_data limit 2;
             select count(*) from raw_csv_data;
            postgres
             docker-compose exec -it reporting_db psql -U reporter -d reports -h localhost -p 5432
             \dt	
             \d transformed_data
             SELECT * FROM transformed_data LIMIT 2;
             SELECT COUNT(*) FROM transformed_data;
    
    step-4
        Go to superset UI http://localhost:8088/ (username: admin, passowd: admin). Import dashboards from ETL_Pipeline/superset_definitions/dashboards.zip enter passowd as reporter_pw and refresh the page.
