
import os
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from urllib.parse import quote_plus

def update(df):
    load_dotenv(override=True)

    # DB 연결
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD"))

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    )

    try:
        # df에서 세션별 클러스터 매핑 생성
        session_cluster_map = dict(zip(df['invest_session_id'], df['cluster_num']))
        
        # 업데이트할 데이터 준비
        update_data = pd.DataFrame(list(session_cluster_map.items()), 
                                 columns=['invest_session_id', 'cluster_num'])

        # 임시 테이블로 업데이트
        update_data.to_sql('temp_update', engine, if_exists='replace', index=False)

        with engine.begin() as conn:  # begin()으로 자동 트랜잭션 관리
            # text()로 쿼리 감싸기 - 핵심 수정사항
            result = conn.execute(text("""
                UPDATE invest_session 
                SET cluster_num = temp_update.cluster_num::uuid
                FROM temp_update
                WHERE invest_session.invest_session_id = temp_update.invest_session_id
            """))
            
            # 임시 테이블 삭제
            conn.execute(text("DROP TABLE temp_update"))
            
            print(f"업데이트된 행 수: {result.rowcount}")
            
            
    except Exception as e:
        print(f"업데이트 중 오류 발생: {e}")
        raise


from main_preprocess import model_preprocess
from main_train import model_train
from main_updateDB import update

df = model_preprocess()
df1 = model_train(df)
update(df1)