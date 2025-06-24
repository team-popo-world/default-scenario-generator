from datetime import datetime, timedelta
from airflow import DAG
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

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


from invest.main_preprocess import model_preprocess # 전처리 모델링
from invest.main_train import model_train  # 모델링.py import 하기
from invest.main_updateDB import update_mongo_data # 분류 결과 몽고db에 update


load_dotenv(override=True)


# 기본 DAG 설정
default_args = {
    'owner': 'invest-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'invest_cluster_pipeline',
    default_args=default_args,
    description='전처리 및 모델링, 전송 파이프라인',
    schedule_interval='0 3 * * *',  # 매일 오전 3시 실행
    catchup=False,
    tags=['preprocessing', 'modeling', 'update'],
)

def preprocess_data(**context):
    try:
        print("데이터 전처리 시작...")
        df = model_preprocess()
        
        if df is None or df.empty:
            raise ValueError("전처리 결과가 비어있습니다")
        
        json_data = df.to_json()
        json_size = len(json_data.encode('utf-8'))
        print(f"전처리 완료. 데이터 크기: {json_size} bytes")
        
        if json_size > 40000:
            print(f"Warning: 데이터 크기가 큽니다 ({json_size} bytes)")
        
        context['ti'].xcom_push(key='preprocessed_df', value=json_data)
        print("전처리 데이터 XCom 푸시 완료")
        
    except Exception as e:
        print(f"전처리 중 오류 발생: {str(e)}")
        raise


def modeling_data(**context):
    try:
        print("모델링 시작...")
        preprocessed_json = context['ti'].xcom_pull(key='preprocessed_df', task_ids='preprocess_data')
        
        if not preprocessed_json:
            raise ValueError("전처리 데이터를 가져올 수 없습니다")
        
        df = pd.read_json(preprocessed_json)
        if df.empty:
            raise ValueError("전처리된 데이터가 비어있습니다")
        
        print(f"모델링 입력 데이터 크기: {len(df)} rows")
        result_df = model_train(df)
        
        if result_df is None or result_df.empty:
            raise ValueError("모델링 결과가 비어있습니다")
        
        result_json = result_df.to_json()
        context['ti'].xcom_push(key='modeling_result', value=result_json)
        print(f"모델링 완료. 결과 데이터 크기: {len(result_df)} rows")
        
        return result_json
        
    except Exception as e:
        print(f"모델링 중 오류 발생: {str(e)}")
        raise


def update_data(**context):
    try:
        print("데이터베이스 업데이트 시작...")
        df_json = context['ti'].xcom_pull(key='modeling_result', task_ids='modeling_data')
        
        if not df_json:
            df_json = context['ti'].xcom_pull(task_ids='modeling_data')
        
        if not df_json:
            raise ValueError("모델링 결과를 가져올 수 없습니다")
        
        df = pd.read_json(df_json)
        if df.empty:
            raise ValueError("업데이트할 데이터가 비어있습니다")
        
        print(f"업데이트할 데이터 크기: {len(df)} rows")
        update_mongo_data(df, "invest_cluster_result")
        print("데이터베이스 업데이트 완료")
        
    except Exception as e:
        print(f"데이터베이스 업데이트 중 오류 발생: {str(e)}")
        raise



# Task 정의
# preprocess_task
# modeling_task
# update_task

# 데이터 전처리 Task
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

# 모델링 Task
modeling_task = PythonOperator(
    task_id='modeling_data',
    python_callable=modeling_data,
    dag=dag
)

# 데이터베이스 업데이트 Task
update_task = PythonOperator(
    task_id='update_data',
    python_callable=update_data,
    dag=dag
)

# Task 의존성 설정
# 데이터 불러오기 >> 데이터 전처리 >> 모델링
# api는 별로도 분리되어있기 때문에 airflow에 작성할 필요없음
# 모델링한 결과를 api로 불러올거라면 여기에 그 부분에 대한 post도 필요하지만 db에 바로 업데이트할 예정이라면 필요 없음

preprocess_task >> modeling_task >> update_task


