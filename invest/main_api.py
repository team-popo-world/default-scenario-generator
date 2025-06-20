from fastapi import FastAPI
from routers import graph, cluster

app = FastAPI(
    title="Graph API",
    version="1.0.0",
    description="그래프 생성 API"
)

app.include_router(graph.router)
# app.include_router(cluster.router)
