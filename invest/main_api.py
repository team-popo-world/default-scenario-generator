from fastapi import FastAPI
from routers import graph, cluster
import pandas as pd

app = FastAPI()

app.include_router(graph.router)
app.include_router(cluster.router)
