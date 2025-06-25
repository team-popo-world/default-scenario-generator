import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
from datetime import datetime

load_dotenv(override=True)

def update_mongo_data(df):
    # MongoDB 연결 정보
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    
    client = MongoClient(uri)
    db = client[db_name]
    collection = db["invest_cluster_result"]

    # json 데이터
    records = df.to_dict('records')

    updated_count = 0
    inserted_count = 0

    for record in records:
        record['updated_at'] = datetime.now()

        # invest_session_id를 기준으로 upsert 수행
        result = collection.update_one(
            {"invest_session_id": record["invest_session_id"]},  # 조건
            {"$set": record},  # 업데이트할 데이터
            upsert=True  # 없으면 새로 생성
        )
        
        if result.upserted_id:
            inserted_count += 1
        elif result.modified_count > 0:
            updated_count += 1

    print(f"업데이트된 document: {updated_count}개")
    print(f"새로 삽입된 document: {inserted_count}개")
    
    # 전체 document 수 확인
    total_count = collection.count_documents({})
    print(f"컬렉션 내 총 document 수: {total_count}개")

    # 첫 번째 document 확인
    first_doc = collection.find_one()
    print("첫 번째 document:", first_doc)


# from main_preprocess import model_preprocess
# from main_train import model_train

# df = model_preprocess()
# df1 = model_train(df)
# update_mongo_data(df1)
# print(df1.info())