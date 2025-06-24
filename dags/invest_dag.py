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

from scenario_app.main import main as generate_scenarios
from scenario_app.send_data import send_data

from invest.main_preprocess import model_preprocess # 전처리 모델링
# from invest.main_train import model_train  # 모델링.py import 하기

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
    schedule_interval='0 9 * * *',  # 매일 오전 9시 실행
    catchup=False,
    tags=['preprocessing', 'modeling', 'mlflow'],
)

def preprocess_data(**context):
    df = model_preprocess()
    context['ti'].xcom_push(key='preprocessed_df', value=df.to_json())  # DataFrame을 JSON 문자열로 변환

def modeling_data(**context):
    preprocessed_json = context['ti'].xcom_pull(key='preprocessed_df', task_ids='preprocess_data')
    df = pd.read_json(preprocessed_json)  # JSON 문자열 → DataFrame
    
    # 실제 모델링 로직이 구현되면 여기서 호출
    # result_df = model_train(df)  # 모델링 함수 호출
    
    # 임시로 원본 DataFrame 반환 (모델링 로직 구현 전까지)
    result_df = df
    
    # 결과를 XCom에 푸시
    context['ti'].xcom_push(key='modeling_result', value=result_df.to_json())
    return result_df.to_json()

def update_data(**context):
    # modeling_data 태스크의 결과를 가져옴
    df_json = context['ti'].xcom_pull(key='modeling_result', task_ids='modeling_data')
    if not df_json:
        # 백업으로 return_value도 체크
        df_json = context['ti'].xcom_pull(task_ids='modeling_data')
    
    df = pd.read_json(df_json)

    load_dotenv(override=True)

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')

    try:
        with engine.begin() as conn:  # 트랜잭션 사용
            update_count = 0
            for _, row in df.iterrows():
                update_query = text("""
                    UPDATE invest_session
                    SET invest_type = :invest_type
                    WHERE invest_session_id = :invest_session_id
                """)
                result = conn.execute(update_query, {
                    "invest_type": row["invest_type"],
                    "invest_session_id": row["invest_session_id"]
                })
                update_count += result.rowcount
        
        print(f"Successfully updated {update_count} rows")
        return f"Update completed: {update_count} rows updated"
    
    except Exception as e:
        print(f"Error during update: {str(e)}")
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