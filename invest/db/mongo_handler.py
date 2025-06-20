import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(override=True)

collection_map = {
    "invest": "INVEST_HISTORY",
    "invest_dummy": "INVEST_HISTORY_DUMMY",
    "quest": "QUEST_HISTORY",
    "saving_account": "SAVING_ACCOUNT_HISTORY"
}

# 불러온 mongoDB 전처리
def mongo_preprocess(df):
    if 'userId' in df.columns:
        df['userId'] = df['userId'].astype(str)

    if 'riskLevel' in df.columns:
        df['riskLevel'] = df['riskLevel'].replace({
            '고위험 고수익': 'high',
            '중위험 균형형': 'mid',
            '저위험 저수익': 'low'
        })

    if all(col in df.columns for col in ['investSessionId', 'riskLevel', 'turn']):
        df.sort_values(by=['investSessionId', 'riskLevel', 'turn'], inplace=True)
        df['deltaShares'] = df.groupby(['investSessionId', 'riskLevel'])['numberOfShares'].diff()
        df['deltaShares'] = df['deltaShares'].fillna(df['numberOfShares'])
        df['deltaShares'] = df['deltaShares'].astype(int)

    return df

def load_mongo_data(fields=None, collection: str = "invest"):
    # MongoDB 연결 정보
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    collection = collection_map.get(collection)
    collection_name = os.getenv(f"{collection}")

    if not collection_name:
        raise ValueError(f"'{collection}'에 해당하는 컬렉션 이름을 찾을 수 없습니다.")
    
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    # fields 리스트를 projection 딕셔너리로 변환
    projection = {field: 1 for field in fields} if fields else None
    if projection is not None:
        projection['_id'] = 0  # 기본적으로 _id는 제외

    df = pd.DataFrame(list(collection.find({}, projection)))
    df = mongo_preprocess(df)

    return df