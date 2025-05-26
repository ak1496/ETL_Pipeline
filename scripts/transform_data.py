
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import md5, col, cast, when
from pyspark.sql.types import StringType, DoubleType

MYSQL_DB_HOST = os.environ.get("MYSQL_DB_HOST", "mysql_db")
MYSQL_DB_PORT = os.environ.get("MYSQL_DB_PORT", "3306")
MYSQL_DB_NAME = os.environ.get("MYSQL_DB_NAME", "raw_data_db")
MYSQL_DB_USER = os.environ.get("MYSQL_DB_USER", "mysql_user")
MYSQL_DB_PASSWORD = os.environ.get("MYSQL_DB_PASSWORD", "mysql_password")
MYSQL_SOURCE_TABLE_NAME = os.environ.get("MYSQL_SOURCE_TABLE_NAME", "raw_csv_data")

PG_REPORTS_DB_HOST = os.environ.get("PG_REPORTS_DB_HOST", "reporting_db")
PG_REPORTS_DB_PORT = os.environ.get("PG_REPORTS_DB_PORT", "5432")
PG_REPORTS_DB_NAME = os.environ.get("PG_REPORTS_DB_NAME", "reports")
PG_REPORTS_DB_USER = os.environ.get("PG_REPORTS_DB_USER", "reporter")
PG_REPORTS_DB_PASSWORD = os.environ.get("PG_REPORTS_DB_PASSWORD", "reporter_pw")
POSTGRES_TARGET_TABLE_NAME = os.environ.get("POSTGRES_TARGET_TABLE_NAME", "transformed_data")

def transform_data_with_pyspark():
    print("Starting Spark transformation...")

    POSTGRES_JDBC_PACKAGE = "org.postgresql:postgresql:42.7.3"
    MYSQL_JDBC_PACKAGE = "mysql:mysql-connector-java:8.0.28"

    spark = SparkSession.builder \
        .appName("DataTransformation") \
        .config("spark.jars.packages", f"{MYSQL_JDBC_PACKAGE},{POSTGRES_JDBC_PACKAGE}") \
        .getOrCreate()

    print("Spark Session created, drivers will be downloaded by Spark.")
    spark.sparkContext.setLogLevel("WARN")

    try:
        print(f"Reading data from MySQL table: {MYSQL_SOURCE_TABLE_NAME}")
        df_spark = spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:mysql://{MYSQL_DB_HOST}:{MYSQL_DB_PORT}/{MYSQL_DB_NAME}") \
            .option("dbtable", MYSQL_SOURCE_TABLE_NAME) \
            .option("user", MYSQL_DB_USER) \
            .option("password", MYSQL_DB_PASSWORD) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .load()

        print("Data loaded from MySQL. Original DataFrame Sample:")
        df_spark.show(5)
        print("Original DataFrame Schema:")
        df_spark.printSchema()

        print("Applying transformations...")

        df_transformed = df_spark

        if "TotalCharges" in df_transformed.columns:
            df_transformed = df_transformed.fillna({'TotalCharges': 0.0})

        if "CustomerID" in df_transformed.columns:
            df_transformed = df_transformed.withColumn(
                "anonymized_CustomerID", md5(col("CustomerID").cast("string"))
            ).drop("CustomerID")

        print("Transformations applied. Transformed DataFrame Sample:")
        df_transformed.show(5)
        print("Transformed DataFrame Schema:")
        df_transformed.printSchema()

        print(f"Writing transformed data to PostgreSQL reporting table: {POSTGRES_TARGET_TABLE_NAME}")
        df_transformed.write \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{PG_REPORTS_DB_HOST}:{PG_REPORTS_DB_PORT}/{PG_REPORTS_DB_NAME}") \
            .option("dbtable", POSTGRES_TARGET_TABLE_NAME) \
            .option("user", PG_REPORTS_DB_USER) \
            .option("password", PG_REPORTS_DB_PASSWORD) \
            .option("driver", "org.postgresql.Driver") \
            .mode("overwrite").save()
        print(f"Successfully wrote transformed data to PostgreSQL table: {POSTGRES_TARGET_TABLE_NAME}")

    except Exception as e:
        print(f"An error occurred during Spark transformation: {e}")
        raise
    finally:
        if 'spark' in locals() and spark:
            spark.stop()
            print("Spark Session stopped.")
