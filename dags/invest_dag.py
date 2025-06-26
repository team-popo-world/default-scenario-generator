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
from invest.utils.data_utils import sanitize_dataframe_for_json, safe_dataframe_to_json

import subprocess
import time
import shutil 
import requests
import psutil


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


def start_mlflow_server():
    """MLflow 서버를 간단하게 시작"""

    # 1. 서버가 이미 실행 중인지 확인
    try:
        response = requests.get("http://43.203.175.69:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ MLflow 서버가 이미 실행 중입니다.")
            return
    except:
        print("MLflow 서버를 시작합니다...")
    
    # 2. MLflow 경로 찾기 (개선된 로직)
    mlflow_path = shutil.which("mlflow")
    if not mlflow_path:
        mlflow_path = "/home/ubuntu/mlflow_env/bin/mlflow"
        if not os.path.exists(mlflow_path):
            print(f"❌ MLflow를 찾을 수 없습니다. 경로를 확인하세요.")
            return
    
    print(f"MLflow 경로: {mlflow_path}")
    
    # 3. 기존 프로세스 정리
    os.system("sudo pkill -f 'mlflow server' 2>/dev/null")
    time.sleep(2)
    
    # 4. MLflow 서버 시작
    try:
        subprocess.Popen([
            mlflow_path, 'server',
            '--host', '0.0.0.0',
            '--port', '5001',
            '--backend-store-uri', 
            'postgresql://postgres:team2%21123@mlflowdb-1.c3gseooicuve.ap-northeast-2.rds.amazonaws.com:5432/mlflowsercer_db',
            '--default-artifact-root', 's3://team2-mlflow-bucket'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 5. 서버 시작 대기
        time.sleep(20)
        
        # 6. 서버 확인
        try:
            response = requests.get("http://localhost:5001/health", timeout=5)
            if response.status_code == 200:
                print("✅ MLflow 서버가 시작되었습니다: http://43.203.175.69:5001")
            else:
                print("⚠️ MLflow 서버 상태 확인 실패")
        except:
            print("⚠️ MLflow 서버 접근 실패")
            
    except Exception as e:
        print(f"❌ MLflow 서버 시작 실패: {e}")



def preprocess_data(**context):
    try:
        print("데이터 전처리 시작...")
        df = model_preprocess()
        
        if df is None:
            raise ValueError("전처리 함수가 None을 반환했습니다")
        
        if df.empty:
            raise ValueError("전처리 결과 DataFrame이 비어있습니다")
            
        # 데이터 품질 검증
        if df.isnull().all().all():
            raise ValueError("전처리 결과가 모두 null 값입니다")
            
        print(f"전처리 완료 - 행 수: {len(df)}, 열 수: {len(df.columns)}")
        
        # **핵심: DataFrame 정리 및 안전한 변환**
        df = sanitize_dataframe_for_json(df)

        print(f"DataFrame 메모리 사용량: {df.memory_usage(deep=True).sum()} bytes")

        # 데이터 크기 확인
        if len(df) > 10000:  # 임계값 설정
            # 디렉토리 생성
            temp_dir = "/opt/airflow/temp_data"
            os.makedirs(temp_dir, exist_ok=True)
            
            # 대용량 데이터는 파일로 저장
            file_path = f"{temp_dir}/preprocessed_{context['ds']}.parquet"
            df.to_parquet(file_path)
            context['ti'].xcom_push(key='data_path', value=file_path)
            print(f"대용량 데이터를 파일로 저장: {file_path}")
        else:
            # 소용량 데이터는 XCom 사용
            # 안전한 JSON 변환
            json_data = safe_dataframe_to_json(df)

            json_size = len(json_data.encode('utf-8'))
            print(f"전처리 완료. 데이터 크기: {json_size} bytes")
            
            # XCom 크기 제한 확인
            if json_size > 1048576:
                temp_dir = "/opt/airflow/temp_data"
                os.makedirs(temp_dir, exist_ok=True)
                file_path = f"{temp_dir}/preprocessed_{context['ds']}.parquet"
                df.to_parquet(file_path)
                context['ti'].xcom_push(key='data_path', value=file_path)
                print(f"XCom 크기 초과로 파일 저장: {file_path}")
            else:
                context['ti'].xcom_push(key='preprocessed_df', value=json_data)
                print("전처리 데이터 XCom 푸시 완료")

    except Exception as e:
        print(f"전처리 실패: {str(e)}")
        raise

def modeling_data(**context):
    try:
        print("모델링 시작...")
        
        # 파일 경로 확인
        data_path = context['ti'].xcom_pull(key='data_path', task_ids='preprocess_data')
        
        if data_path:
            # 파일에서 데이터 로드
            df = pd.read_parquet(data_path)
            print(f"파일에서 데이터 로드: {data_path}")
        else:
            # XCom에서 데이터 로드
            json_data = context['ti'].xcom_pull(key='preprocessed_df', task_ids='preprocess_data')
            if not json_data:
                raise ValueError("전처리된 데이터를 가져올 수 없습니다")
            df = pd.read_json(json_data)
            print("XCom에서 데이터 로드")

        if df.empty:
            raise ValueError("전처리된 데이터가 비어있습니다")
        
        print(f"모델링 입력 데이터 크기: {len(df)} rows")
        result_df = model_train(df)
        
        if result_df is None or result_df.empty:
            raise ValueError("모델링 결과가 비어있습니다")
        
        print(f"모델링 완료. 결과 데이터 크기: {len(result_df)} rows")
        
        # **결과 데이터도 인코딩 정리**
        result_df = sanitize_dataframe_for_json(result_df)
        
        # 결과 데이터 저장
        if len(result_df) > 10000:
            # 대용량 데이터는 파일로 저장
            temp_dir = "/opt/airflow/temp_data"
            os.makedirs(temp_dir, exist_ok=True)
            file_path = f"{temp_dir}/modeling_result_{context['ds']}.parquet"
            result_df.to_parquet(file_path)
            context['ti'].xcom_push(key='result_path', value=file_path)
            print(f"대용량 모델링 결과를 파일로 저장: {file_path}")
        else:
            # **안전한 JSON 변환 사용**
            result_json = safe_dataframe_to_json(result_df)
            context['ti'].xcom_push(key='modeling_result', value=result_json)
            print("모델링 결과 XCom 푸시 완료")
        
        return "modeling_completed"
        
    except Exception as e:
        print(f"모델링 실패: {str(e)}")
        raise


def update_data(**context):
    try:
        print("데이터베이스 업데이트 시작...")
        
        # 파일 경로 확인
        result_path = context['ti'].xcom_pull(key='result_path', task_ids='modeling_data')
        
        if result_path:
            # 파일에서 데이터 로드
            df = pd.read_parquet(result_path)
            print(f"파일에서 데이터 로드: {result_path}")
        else:
            # XCom에서 데이터 로드
            json_data = context['ti'].xcom_pull(key='modeling_result', task_ids='modeling_data')
            if not json_data:
                raise ValueError("모델링 결과를 가져올 수 없습니다")
            df = pd.read_json(json_data)
            print("XCom에서 데이터 로드")

        if df is None or df.empty:
            raise ValueError("업데이트할 데이터가 없습니다")
 
        print(f"업데이트할 데이터 크기: {len(df)} rows")
        update_mongo_data(df)
        print("데이터베이스 업데이트 완료")
        
    except Exception as e:
        print(f"데이터베이스 업데이트 실패: {str(e)}")
        raise

def cleanup_temp_files(**context):
    """임시 파일 정리"""
    try:
        temp_dir = "/opt/airflow/temp_data"
        if os.path.exists(temp_dir):
            files_deleted = 0
            for file in os.listdir(temp_dir):
                if context['ds'] in file:  # 해당 날짜의 파일만 삭제
                    file_path = os.path.join(temp_dir, file)
                    os.remove(file_path)
                    print(f"임시 파일 삭제: {file}")
                    files_deleted += 1
            
            if files_deleted == 0:
                print("삭제할 임시 파일이 없습니다.")
            else:
                print(f"총 {files_deleted}개의 임시 파일을 삭제했습니다.")
        else:
            print("임시 디렉토리가 존재하지 않습니다.")
            
    except Exception as e:
        print(f"임시 파일 정리 중 오류 발생: {str(e)}")
        # 정리 작업 실패는 전체 파이프라인을 중단시키지 않음

# Task 정의

# MLflow 서버 시작
start_mlflow_task = PythonOperator(
    task_id='start_mlflow_server',
    python_callable=start_mlflow_server,
    dag=dag
)

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

# 임시 파일 정리 Task
cleanup_task = PythonOperator(
    task_id='cleanup_temp_files',
    python_callable=cleanup_temp_files,
    dag=dag,
    trigger_rule='all_done'  # 성공/실패 관계없이 실행
)

# Task 의존성 설정
start_mlflow_task >> preprocess_task >> modeling_task >> update_task >> cleanup_task
