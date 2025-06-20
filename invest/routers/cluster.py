# from fastapi import APIRouter
# from pydantic import BaseModel
# import joblib
# import pandas as pd
# import uuid

# router = APIRouter(prefix="/api/cluster")

# # 모델 로드
# model = joblib.load("models/random_forest_model.pkl")

# # 입력 데이터 스키마 정의
# class InputData(BaseModel):
#     InvestSessionId: uuid
#     userId: uuid
#     sex: str
#     age: int
#     chapterId: str
#     tradingTurn: float
#     transactionNum: float
#     avgCashRatio: float
#     avgStayTime: float
#     avgTradeRatio: float
#     tagAvgStayTime: float
#     betShares: float
#     betBuyRatio: float
#     betSellRatio: float

# @router.post("/invest")
# def predict(data: InputData):
#     input_df = pd.DataFrame([data.dict()])  # 한 개 데이터만 처리
#     prediction = model.predict(input_df)
#     return {"predicted_investType": prediction[0]}