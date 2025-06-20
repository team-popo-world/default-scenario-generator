# 평균 현금잔여율
def avg_cash_ratio(df):
    acr = df[['investSessionId', 
              'userId',
              'age',
              'seedMoney',
              'chapterId',
              'turn',
              'currentPoint',
              'startedAt']].copy()

    acr = acr.groupby(['investSessionId', 'userId', 'age'])['currentPoint'].mean().reset_index(name='avgCurrentPoint')
    seed = df[['investSessionId', 'userId', 'seedMoney']].drop_duplicates()
    acr = acr.merge(seed, on=['investSessionId', 'userId'], how='left')

    # startedAt: 각 investSessionId의 첫 턴 startedAt 사용
    started_at = df.sort_values(['investSessionId', 'startedAt']) \
                   .groupby(['investSessionId', 'userId'])['startedAt'] \
                   .first().reset_index()

    acr = acr.merge(started_at, on=['investSessionId', 'userId'], how='left')

    # 현금 잔여율 계산
    acr['avgCashRatio'] = (acr['seedMoney'] - acr['avgCurrentPoint']) / acr['seedMoney']

    averageCashRatio = acr[['investSessionId', 'userId', 'age', 'startedAt', 'avgCashRatio']].copy()
        
    return averageCashRatio