
import os
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from urllib.parse import quote_plus

from main_train import model_train

load_dotenv(override=True)

# DB 연결
host=os.getenv("DB_HOST")
port=os.getenv("DB_PORT")
dbname=os.getenv("DB_NAME")
user=os.getenv("DB_USER")
password=quote_plus(os.getenv("DB_PASSWORD"))

engine = create_engine(
f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
)

# 클러스터링 결과 df 가져오기
cluster_df = model_train()

# 컬럼명 변경
cluster_df = cluster_df.rename(columns={'investSessionId': 'invest_session_id'})


# 클러스터 결과를 임시 테이블에 저장한 뒤 invest_session 테이블이랑 병합
try:
    with engine.connect() as conn:
        # 임시 테이블에 데이터 삽입
        cluster_df.to_sql('temp_cluster_update', conn, if_exists='replace', index=False)
        
        # JOIN을 사용한 대량 업데이트
        update_query = text("""
            UPDATE invest_session 
            SET cluster_num = temp.cluster_num
            FROM temp_cluster_update temp
            WHERE invest_session.invest_session_id = temp.invest_session_id
        """)
        
        result = conn.execute(update_query)
        conn.commit()
        
        # 임시 테이블 삭제
        conn.execute(text("DROP TABLE temp_cluster_update"))
        conn.commit()
        
        print(f"{result.rowcount}개의 레코드가 성공적으로 업데이트되었습니다.")
        
except Exception as e:
    print(f"업데이트 중 오류 발생: {e}")
finally:
    engine.dispose()