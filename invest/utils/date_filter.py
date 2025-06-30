from datetime import datetime, timedelta
import pandas as pd

def filter_date(df):
    # 날짜 컬럼을 datetime으로 변환
    df["startedAt"] = pd.to_datetime(df["startedAt"], errors="coerce")

    # 오늘 자정과 7일 전 자정 계산
    today = datetime.now().date()
    start_date = today - timedelta(days=6)  # 오늘 포함 7일
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(today, datetime.max.time())

     # 필터링: start_date ~ 오늘 자정까지 (시간 포함)
    df = df[(df["startedAt"] >= start_datetime) & (df["startedAt"] <= end_datetime)]

    return df