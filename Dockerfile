# Use the official Airflow image as a base
FROM apache/airflow:2.8.1-python3.10

# Switch to root user temporarily to install system packages
USER root

# Install wget and unzip
RUN apt-get update -yqq && \
    apt-get install -yqq --no-install-recommends wget unzip && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Default OpenJDK JDK (a full JDK, which Spark needs)
RUN apt-get update -yqq && \
    apt-get install -yqq --no-install-recommends default-jdk && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable for Spark dynamically
ENV JAVA_HOME /usr/lib/jvm/default-java
ENV PATH $PATH:$JAVA_HOME/bin

# Switch back to the Airflow user
ARG AIRFLOW_UID=50000
ENV AIRFLOW_UID=${AIRFLOW_UID}
USER ${AIRFLOW_UID}

# Create a directory for JDBC drivers
RUN mkdir -p /opt/airflow/jdbc
RUN wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar -P /opt/airflow/jdbc/
RUN wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar -P /opt/airflow/jdbc/

WORKDIR /opt/airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 777 /opt/airflow/logs
