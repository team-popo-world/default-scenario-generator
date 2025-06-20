from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import logging

from scenario_app.main import main as generate_scenarios
from scenario_app.send_data import send_data

from invest.main_preprocess import cluster_preprocess # 전처리 모델링
# from invest # 모델링.py import 하기

# 기본 DAG 설정
default_args = {
    'owner': 'scenario-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'scenario_generation_pipeline',
    default_args=default_args,
    description='시나리오 생성 및 전송 파이프라인',
    schedule_interval='0 9 * * *',  # 매일 오전 9시 실행
    catchup=False,
    tags=['scenario', 'generation', 'json'],
)

def preprocess_data(d):
    return d

def modeling_data(theme):
    return theme

def update_data(x):
    return x

# Task 정의
# preprocess_task
# modeling_task
# update_task

# 데이터 전처리 Task
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data(),
    dag=dag
)

# 모델링 Task
modeling_task = PythonOperator(
    task_id='modeling_data',
    python_callable=modeling_data(),
    dag=dag
)

# 데이터베이스 업데이트 Task
update_task = PythonOperator(
    task_id='update_data',
    python_callable=update_data(),
    dag=dag
)

# Task 의존성 설정
# 데이터 불러오기 >> 데이터 전처리 >> 모델링
# api는 별로도 분리되어있기 때문에 airflow에 작성할 필요없음
# 모델링한 결과를 api로 불러올거라면 여기에 그 부분에 대한 post도 필요하지만 db에 바로 업데이트할 예정이라면 필요 없음

preprocess_task >> modeling_task >> update_task