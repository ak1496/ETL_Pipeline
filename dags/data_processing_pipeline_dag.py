from __future__ import annotations
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from scripts.load_data import load_csv_to_mysql
from scripts.transform_data import transform_data_with_pyspark

with DAG(
    dag_id="data_processing_pipeline_dag",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["data_pipeline", "transformation", "pyspark", "mysql", "postgres", "reporting"],
) as dag:

    load_raw_data_task = PythonOperator(
        task_id="load_csv_to_mysql_task",
        python_callable=load_csv_to_mysql,
    )

    transform_data_task = PythonOperator(
        task_id="transform_data_with_pyspark_task",
        python_callable=transform_data_with_pyspark,
    )

    load_raw_data_task >> transform_data_task