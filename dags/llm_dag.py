from datetime import datetime, timedelta
from airflow import DAG
import pandas as pd
import os
import logging
from pymongo import MongoClient
from report_llm.utils.load_db import load_userId, load_data
from report_llm.utils.llm import get_llm_chain
from report_llm.main import generate_and_update
# Airflow 버전 호환성을 위한 PythonOperator import
try:
    # Airflow 3.0+ 버전용 (표준 프로바이더)
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:
    try:
        # Airflow 2.8+ 버전용 (기존 경로)
        from airflow.operators.python import PythonOperator
    except ImportError:
        # Airflow 2.7 이하 버전용
        from airflow.operators.python_operator import PythonOperator

# 기본 DAG 설정
default_args = {
    'owner': 'llm-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weekly_analysis_update_pipeline', # DAG 이름 (Airflow UI에 표시)
    default_args=default_args,
    description='아이 레포트 생성 및 업데이트 파이프라인', # 설명 (UI용)
    schedule_interval='0 0 * * 1',  # 실행 주기: 매주 월요일 자정 (cron 형식)
    catchup=False, # 과거 누락된 실행 여부 무시 (False면 현재 시점부터 실행)
    tags=['scenario', 'generation', 'json'], # UI에서 DAG 태그로 필터링 가능
)

# api 불러오기 -> llm으로 report 생성 -> DB에 업데이트
def call_api(ti):
    user_list = load_userId()
    invest_merged_df, quest_merged_df, shop_merged_df, cluster_df = load_data(user_list)
    
    # XCom으로 푸시
    ti.xcom_push(key="user_list", value=user_list)
    ti.xcom_push(key="invest_merged_df", value=invest_merged_df.to_json())
    ti.xcom_push(key="quest_merged_df", value=quest_merged_df.to_json())
    ti.xcom_push(key="shop_merged_df", value=shop_merged_df.to_json())
    ti.xcom_push(key="cluster_df", value=cluster_df.to_json())

def generate_analysis_and_update(ti):
    # XCom에서 데이터 로드
    user_list = ti.xcom_pull(key="user_list", task_ids='call_api_task')
    invest_merged_df = pd.read_json(ti.xcom_pull(key="invest_merged_df", task_ids='call_api_task'))
    quest_merged_df = pd.read_json(ti.xcom_pull(key="quest_merged_df", task_ids='call_api_task'))
    shop_merged_df = pd.read_json(ti.xcom_pull(key="shop_merged_df", task_ids='call_api_task'))
    cluster_df = pd.read_json(ti.xcom_pull(key="cluster_df", task_ids='call_api_task'))

    chain = get_llm_chain()

    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")

    client = MongoClient(uri) 
    db = client[db_name]
    user_collection = db["user_analysis"]
    graph_collection = db["user_graph"]

    for userId in user_list:
        generate_and_update(userId, chain, invest_merged_df, cluster_df, quest_merged_df, shop_merged_df, user_collection, graph_collection)

# Task 정의
call_api_task = PythonOperator(
    task_id='call_api',
    python_callable=call_api,
    provide_context=True,
    dag=dag,
)

generate_and_update_task = PythonOperator(
    task_id='generate_analysis_and_update',
    python_callable=generate_analysis_and_update,
    provide_context=True,
    dag=dag,
)

# Task 의존성 설정
# api 불러오기 -> llm으로 report 생성 & DB에 업데이트
call_api_task >> generate_and_update_task