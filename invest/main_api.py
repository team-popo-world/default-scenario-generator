from fastapi import FastAPI
from invest.routers import graph, cluster
import os
from dotenv import load_dotenv

app = FastAPI(
    title="Graph API",
    version="1.0.0",
    description="그래프 생성 API"
)

app.include_router(graph.router)
# app.include_router(cluster.router)


# 환경변수 로드
load_dotenv()

# 데이터베이스 설정 확인
print(f"MongoDB URI: {os.getenv('MONGODB_URI')}")