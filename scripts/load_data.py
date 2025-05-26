import pandas as pd
from sqlalchemy import create_engine

CSV_FILE_PATH = "/opt/airflow/csv_data/customer_churn_data.csv"
MYSQL_RAW_TABLE_NAME = "raw_csv_data"

MYSQL_HOST = "mysql_db"
MYSQL_PORT = "3306"
MYSQL_DB = "raw_data_db"
MYSQL_USER = "mysql_user"
MYSQL_PASSWORD = "mysql_password"

def load_csv_to_mysql():

    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

    try:
        print(f"Attempting to read CSV from: {CSV_FILE_PATH}")
        df = pd.read_csv(CSV_FILE_PATH)
        print(f"Successfully read CSV. DataFrame head:\n{df.head()}")

        print(f"Attempting to write DataFrame to MySQL table: {MYSQL_RAW_TABLE_NAME}")
        df.to_sql(MYSQL_RAW_TABLE_NAME, engine, if_exists='replace', index=False)
        print(f"Successfully loaded data into MySQL table: {MYSQL_RAW_TABLE_NAME}")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_FILE_PATH}. Please ensure it exists.")
        raise
    except Exception as e:
        print(f"An error occurred while loading data to MySQL: {e}")
        raise