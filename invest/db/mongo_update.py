import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict

load_dotenv(override=True)

def update_mongo_data(user_id: str, json_data: List[Dict], collection_name: str):
    # MongoDB 연결 정보
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    document = {
        "userId": user_id,
        "data": json_data,
        "updatedAt": datetime.utcnow()
    }

    collection.insert_one(document)