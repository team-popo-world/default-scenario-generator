FROM apache/airflow:2.8.0-python3.10

USER root
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt /

# airflow 유저로 pip install!
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt

# 나머지 COPY 등은 계속 airflow 유저 상태로
COPY scenario_app /opt/airflow/scenario_app
COPY dags /opt/airflow/dags