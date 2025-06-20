FROM apache/airflow:2.8.0-python3.10

USER root
RUN apt-get update && apt-get install -y build-essential curl
# APT 미러 서버 교체 (예: 한국 카카오 미러)
# RUN sed -i 's|http://deb.debian.org|http://mirror.kakao.com|g' /etc/apt/sources.list \
#  && apt-get update \
#  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential curl \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/*

ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
ENV AIRFLOW__CORE__PLUGINS_FOLDER=/opt/airflow/plugins

# airflow 유저로 pip install!
USER airflow
RUN pip install --no-cache-dir -r /requirements.txt

# 나머지 COPY 등은 계속 airflow 유저 상태로
COPY scenario_app /opt/airflow/scenario_app
COPY invest /opt/airflow/invest
COPY dags /opt/airflow/dags
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# 포트 열기 (FastAPI)
EXPOSE 8001
EXPOSE 8080
ENTRYPOINT []

# uvicorn FastAPI 실행 (백그라운드) + airflow 웹서버 실행
# => docker-compose로 airflow scheduler/webserver 따로 실행 가능
# CMD ["sh", "-c", "uvicorn invest.main_api:app --host 0.0.0.0 --port 8000 & airflow webserver"] -> EntryPoint에서 실행
