import pandas as pd

def time_type(df):
    # dt 타입 초단위로 변환
    df['tagAvgStayTime'] = df['tagAvgStayTime'].dt.total_seconds()

    # 기준 날짜 설정
    today = pd.Timestamp.now()

    # 일수 차이로 변환
    df['daysSinceStart'] = (today - df['createdAt']).dt.days
    df.drop("createdAt", axis=1, inplace=True)

    return df