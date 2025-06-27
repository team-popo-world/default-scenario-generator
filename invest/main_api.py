from fastapi import FastAPI
from invest.routers import graph, cluster
import os
from dotenv import load_dotenv
import logging

# 환경변수 로드 (최우선으로 실행)
load_dotenv(override=True)

# 환경변수 확인 로그
print(f"MONGO_URI: {os.getenv('MONGO_URI')}")
print(f"MONGO_DB_NAME: {os.getenv('MONGO_DB_NAME')}")
print(f"INVEST_CLUSTER_RESULT: {os.getenv('INVEST_CLUSTER_RESULT')}")

app = FastAPI(
    title="Graph API",
    version="1.0.0",
    description="그래프 생성 API"
)

app.include_router(graph.router)
# app.include_router(cluster.router)




# 데이터베이스 설정 확인
print(f"MongoDB URI: {os.getenv('MONGODB_URI')}")