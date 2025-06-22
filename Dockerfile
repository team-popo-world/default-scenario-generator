FROM apache/airflow:2.8.1-python3.10

USER root
RUN apt-get update && apt-get install -y build-essential curl && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
ENV AIRFLOW__CORE__PLUGINS_FOLDER=/opt/airflow/plugins
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
ENV PYTHONPATH=/opt/airflow:$PYTHONPATH

# airflow 유저로 pip install!
USER airflow
COPY requirements.airflow.txt /opt/airflow/
RUN pip install --no-cache-dir -r requirements.airflow.txt

# 프로젝트 파일 복사
COPY --chown=airflow:root scenario_app /opt/airflow/scenario_app
COPY --chown=airflow:root dags /opt/airflow/dags
COPY --chown=airflow:root invest /opt/airflow/invest

# 환경설정 파일 복사 (필요시)
COPY --chown=airflow:root .env /opt/airflow/.env

# 디렉토리 생성
RUN mkdir -p /opt/airflow/logs /opt/airflow/news_json_files /opt/airflow/result_json_files
# 포트 열기 (Airflow 웹서버)
EXPOSE 8080

# 기본 entrypoint는 airflow 이미지의 기본값 사용
