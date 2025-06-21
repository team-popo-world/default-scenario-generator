FROM apache/airflow:2.8.0-python3.10

USER root
RUN apt-get update && apt-get install -y build-essential curl

ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
ENV AIRFLOW__CORE__PLUGINS_FOLDER=/opt/airflow/plugins

# airflow 유저로 pip install!
USER airflow
COPY requirements.airflow.txt /opt/airflow/
RUN pip install --no-cache-dir -r requirements.airflow.txt

# 나머지 COPY 등은 계속 airflow 유저 상태로
COPY scenario_app /opt/airflow/scenario_app
COPY dags /opt/airflow/dags
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# 포트 열기 (FastAPI)
EXPOSE 8080

# uvicorn FastAPI 실행 (백그라운드) + airflow 웹서버 실행
# => docker-compose로 airflow scheduler/webserver 따로 실행 가능
