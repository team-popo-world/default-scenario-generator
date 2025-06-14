from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import logging

from scenario_app.main import main as generate_scenarios
from scenario_app.send_data import send_data

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

def clean_json_files():
    """news_json_files와 result_json_files 디렉토리의 모든 파일 삭제"""
    # 현재 파일(scenario_generator_dag.py) 기준으로 scenario_app 경로 구성
    dag_path = os.path.dirname(os.path.abspath(__file__))
    scenario_app_path = os.path.join(dag_path, "..", "scenario_app")
    scenario_app_path = os.path.abspath(scenario_app_path)  # 절대경로로 변환

    dirs_to_clean = ['news_json_files', 'result_json_files']
    for dir_name in dirs_to_clean:
        dir_path = os.path.join(scenario_app_path, dir_name)
        if os.path.exists(dir_path):
            # 디렉토리 내의 모든 파일과 하위 디렉토리 삭제
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    logging.info(f"삭제됨: {file_path}")
                # 빈 하위 디렉토리도 삭제
                for dir in dirs:
                    dir_path_to_remove = os.path.join(root, dir)
                    if not os.listdir(dir_path_to_remove):  # 빈 디렉토리인 경우
                        os.rmdir(dir_path_to_remove)
                        logging.info(f"빈 디렉토리 삭제됨: {dir_path_to_remove}")
        else:
            logging.info(f"디렉토리가 존재하지 않음: {dir_path}")
    logging.info("파일 정리 완료")

def generate_theme_scenarios(theme):
    """특정 테마의 시나리오 10개 생성"""
    def _generate():
        logging.info(f"{theme} 테마 시나리오 생성 시작")
        try:
            generate_scenarios(theme, 10)
            logging.info(f"{theme} 테마 시나리오 생성 완료")
        except Exception as e:
            logging.error(f"{theme} 테마 시나리오 생성 실패: {e}")
            raise
    return _generate

def send_all_scenarios():
    """생성된 모든 시나리오 전송"""
    logging.info("시나리오 전송 시작")
    try:
        send_data()
        logging.info("시나리오 전송 완료")
    except Exception as e:
        logging.error(f"시나리오 전송 실패: {e}")
        raise

# Task 정의
clean_task = PythonOperator(
    task_id='clean_json_files',
    python_callable=clean_json_files,
    dag=dag,
)

# 각 테마별 시나리오 생성 Task
themes = ['pig', 'food', 'magic', 'moon']
generation_tasks = []

for theme in themes:
    task = PythonOperator(
        task_id=f'generate_{theme}_scenarios',
        python_callable=generate_theme_scenarios(theme),
        dag=dag,
    )
    generation_tasks.append(task)

# 시나리오 전송 Task
send_task = PythonOperator(
    task_id='send_scenarios',
    python_callable=send_all_scenarios,
    dag=dag,
)

# Task 의존성 설정
# 1. 먼저 파일 정리
# 2. 모든 테마의 시나리오를 병렬로 생성
# 3. 모든 생성이 완료되면 전송
clean_task >> generation_tasks >> send_task