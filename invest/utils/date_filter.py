from datetime import datetime, timedelta
import pandas as pd

def filter_date(df):
    # 날짜 컬럼을 datetime으로 변환
    df["startedAt"] = pd.to_datetime(df["startedAt"])

    # 현재 날짜와 일주일 전 날짜 계산
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)

    # 필터링: 일주일 전부터 오늘까지
    df = df[(df["startedAt"] >= one_week_ago) & (df["startedAt"] <= now)]

    return df