import pandas as pd

# 평균 턴 체류시간
def avg_stay_time(df):
    turn = df[['investSessionId',
               'userId',
               'age',
                'turn',
                'startedAt',
                'endedAt']].copy()

    # 문자열을 datetime으로 변환
    turn['startedAt'] = pd.to_datetime(turn['startedAt'], errors='coerce')
    turn['endedAt'] = pd.to_datetime(turn['endedAt'], errors='coerce')

    turn['stayTime'] = (turn['endedAt'] - turn['startedAt']).dt.total_seconds()

    # 평균 체류 시간 계산
    avg_time = (
        turn
        .drop_duplicates(subset=['investSessionId', 'turn'])
        .groupby(['investSessionId', 'userId', 'age'])['stayTime']
        .mean()
        .reset_index(name='avgStayTime')
    )

    # 각 그룹의 첫 startedAt 추출
    first_start = (
        turn
        .sort_values(by='turn')
        .groupby(['investSessionId', 'userId', 'age'])
        .first()
        .reset_index()[['investSessionId', 'userId', 'age', 'startedAt']]
    )

    # 평균 체류 시간과 첫 startedAt 병합
    avgStayTime = pd.merge(avg_time, first_start, on=['investSessionId', 'userId', 'age'])

    return avgStayTime