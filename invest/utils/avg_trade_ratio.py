import numpy as np
import pandas as pd

# 각 위험 별 구매/판매 비율
def avg_buy_ratio(df):
    # 구매 데이터 생성
    transcation_df = df[['investSessionId',
                        'userId',
                        'age',
                        'turn',
                        'riskLevel',
                        'numberOfShares',
                        'deltaShares',
                        'startedAt']].copy()
    
    # 변화량에 따라 BUY/SELL 구분하기
    transcation_df['is_buy'] = np.where(
        transcation_df['deltaShares'] > 0, 
        transcation_df['deltaShares'], 
        0
    )

    # 각 investSessionId, riskLevel 별로 buy/sell 개수 집계
    buy_sell_counts = transcation_df.groupby(['investSessionId', 'userId', 'riskLevel', 'age'])[['is_buy']].sum().reset_index()
    buy_sell_counts.rename(columns={'is_buy': 'buyCount'}, inplace=True)

    # investSessionId별 전체 buy_count, sell_count 구하기
    total_buy = buy_sell_counts.groupby(['investSessionId', 'userId', 'age'])['buyCount'].sum().reset_index(name='totalBuyCount')

    # 원본과 병합
    buy_sell_counts = buy_sell_counts.merge(total_buy, on=['investSessionId', 'userId', 'age'])
    buy_sell_counts['buyRatio'] = buy_sell_counts['buyCount'] / buy_sell_counts['totalBuyCount']

    # buy_ratio_pivot: 열로 riskLevel을 펼치기 
    buy_ratio_pivot = buy_sell_counts.pivot(
        index=["investSessionId", "userId", "age"],
        columns='riskLevel',
        values='buyRatio'
    ).fillna(0)

    buy_ratio_pivot.columns = [f"{level}BuyRatio" for level in buy_ratio_pivot.columns]
    buy_ratio_pivot.reset_index(inplace=True)

    # 첫 startedAt 값 추가
    started_at = transcation_df.groupby(['investSessionId', 'userId'])['startedAt'].first().reset_index()
    buy_ratio_pivot = buy_ratio_pivot.merge(started_at, on=['investSessionId', 'userId'], how='left')

    print("buyRatioPivot", buy_ratio_pivot)

    return  buy_ratio_pivot

def avg_sell_ratio(df):
    # 판매 데이터 생성
    transcation_df = df[['investSessionId',
                        'userId',
                        'age',
                        'turn',
                        'riskLevel',
                        'numberOfShares',
                        'deltaShares',
                        'startedAt']].copy()
    
    # 변화량에 따라 BUY/SELL 구분하기
    transcation_df['is_sell'] = np.where(
        transcation_df['deltaShares'] < 0, 
        -transcation_df['deltaShares'],
        0
    )

    # 각 investSessionId, riskLevel 별로 buy/sell 개수 집계
    buy_sell_counts = transcation_df.groupby(['investSessionId', 'userId', 'riskLevel', 'age'])[['is_sell']].sum().reset_index()
    buy_sell_counts.rename(columns={'is_sell': 'sellCount'}, inplace=True)

    # investSessionId별 전체 buy_count, sell_count 구하기
    total_sell = buy_sell_counts.groupby(['investSessionId', 'userId', 'age'])['sellCount'].sum().reset_index(name='totalSellCount')

    # 원본과 병합
    buy_sell_counts = buy_sell_counts.merge(total_sell, on=['investSessionId', 'userId', 'age'])
    buy_sell_counts['sellRatio'] = buy_sell_counts['sellCount'] / buy_sell_counts['totalSellCount']

    # sell_ratio pivot: 열로 riskLevel을 펼치기
    sell_ratio_pivot = buy_sell_counts.pivot(
        index=["investSessionId", "userId", "age"],
        columns='riskLevel',
        values='sellRatio'
    ).fillna(0)
    sell_ratio_pivot.columns = [f"{level}SellRatio" for level in sell_ratio_pivot.columns]
    sell_ratio_pivot.reset_index(inplace=True)

    # 첫 startedAt 값 추가
    started_at = transcation_df.groupby(['investSessionId', 'userId'])['startedAt'].first().reset_index()
    sell_ratio_pivot = sell_ratio_pivot.merge(started_at, on=['investSessionId', 'userId'], how='left')

    print("sellRatioPivot", sell_ratio_pivot)

    return sell_ratio_pivot

def avg_trade_ratio(buy, sell):
    # transcation_df = df[['investSessionId',
    #                     'userId',
    #                     'age',
    #                     'turn',
    #                     'riskLevel',
    #                     'numberOfShares',
    #                     'deltaShares']].copy()
    
    # merge 두 pivot
    avgTradeRatio = pd.merge(buy, sell, on=["investSessionId", "userId", "age", "startedAt"])
    # avgTradeRatio.drop(columns="startedAt", inplace=True)
    print("avgTradeRatio", avgTradeRatio)
    # user_info = transcation_df.groupby(["investSessionId", "userId"])['age'].first().reset_index()
    # avgTradeRatio = avgTradeRatio.merge(user_info, on=["investSessionId", "userId", "age"], how='left')

    return avgTradeRatio