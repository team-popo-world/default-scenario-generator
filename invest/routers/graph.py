from fastapi import APIRouter
from fastapi.responses import JSONResponse
from invest.utils.make_graph import make_avg_stay_time, make_buy_ratio, make_sell_ratio, make_buy_sell_ratio, make_bet_ratio, make_avg_cash_ratio, make_invest_style
from invest.db.mongo_update import update_mongo_data

router = APIRouter(prefix="/api/invest")

@router.get("/avg_stay_time/all")
def avg_stay_time_all(userId :str):
    df = make_avg_stay_time(userId, filter=False)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json

@router.get("/avg_stay_time/week")
def avg_stay_time_week(userId :str):
    df = make_avg_stay_time(userId, filter=True)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json

@router.get("/buy_ratio/all")
def buy_ratio_all(userId :str):
    df = make_buy_ratio(userId, filter=False)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json

@router.get("/buy_ratio/week")
def buy_ratio_week(userId :str):
    df = make_buy_ratio(userId, filter=True)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json

@router.get("/sell_ratio/all")
def sell_ratio_all(userId :str):
    df = make_sell_ratio(userId, filter=False)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json

@router.get("/sell_ratio/week")
def sell_ratio_week(userId :str):
    df = make_sell_ratio(userId, filter=True)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json

@router.get("/buy_sell_ratio/all")
def buy_sell_ratio_all(userId :str):
    df = make_buy_sell_ratio(userId, filter=False)
    fin_df = df.drop_duplicates()
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = fin_df.to_dict(orient="records")
    return json

@router.get("/buy_sell_ratio/week")
def buy_sell_ratio_week(userId :str):
    df = make_buy_sell_ratio(userId, filter=True) 
    fin_df = df.drop_duplicates()   
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = fin_df.to_dict(orient="records")
    return json

@router.get("/bet_ratio/all")
def bet_ratio_all(userId :str):
    try:
        df = make_bet_ratio(userId, filter=False)
        if df.empty:
            return JSONResponse(content={"message": "데이터가 없습니다.", "userId": userId}, status_code=200)
        # 👉 추가적인 직렬화 안전 처리
        df = df.fillna("")
        if "startedAt" in df.columns:
            df["startedAt"] = df["startedAt"].astype(str)
        df["userId"] = df["userId"].astype(str)
        return JSONResponse(content=df.to_dict(orient="records"), status_code=200)
    except Exception as e:
        print(f"[API ERROR] /bet_ratio/all failed for userId {userId}: {e}")
        return JSONResponse(
            status_code=200,
            content={"userId": userId, "data": [], "error": str(e)}
        )

@router.get("/bet_ratio/week")
def bet_ratio_week(userId :str):
    try:
        df = make_bet_ratio(userId, filter=True)
        if df.empty:
            return JSONResponse(content={"message": "데이터가 없습니다.", "userId": userId}, status_code=200)
        # 👉 추가적인 직렬화 안전 처리
        df = df.fillna("")
        if "startedAt" in df.columns:
            df["startedAt"] = df["startedAt"].astype(str)
        df["userId"] = df["userId"].astype(str)
        return JSONResponse(content=df.to_dict(orient="records"), status_code=200)
    except Exception as e:
        print(f"[API ERROR] /bet_ratio/week failed for userId {userId}: {e}")
        return JSONResponse(
            status_code=200,
            content={"userId": userId, "data": [], "error": str(e)}
        )

@router.get("/avg_cash_ratio/all")
def avg_cash_ratio_all(userId :str):
    df = make_avg_cash_ratio(userId, filter=False)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json

@router.get("/avg_cash_ratio/week")
def avg_cash_ratio_week(userId :str):
    df = make_avg_cash_ratio(userId, filter=True)
    if df.empty:
        return JSONResponse(
            content={"message": "데이터가 없습니다.", "userId": userId},
            status_code=200  # 👈 여기 중요!
        )
    json = df.to_dict(orient="records")
    return json



@router.get("/invest_style/all")
def invest_style_all(userId: str):   
    try:
        df = make_invest_style(userId, filter=False)
        if df.empty:
            return {"message": "데이터가 없습니다.", "userId": userId}
        
        json_data = df.to_dict(orient="records")
        return json_data
        
    except Exception as e:
        return {"error": str(e), "userId": userId}

@router.get("/invest_style/week")
def invest_style_week(userId :str):
    try:
        df = make_invest_style(userId, filter=True)
        if df.empty:
            return {"message": "데이터가 없습니다.", "userId": userId}
        
        json_data = df.to_dict(orient="records")
        return json_data
        
    except Exception as e:
        return {"error": str(e), "userId": userId}
