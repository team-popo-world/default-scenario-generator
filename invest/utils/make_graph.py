import pandas as pd
from invest.db.mongo_handler import load_mongo_data
from invest.db.postgres_handler import load_postgres_data
from invest.db.merge_df import load_invest_df
from invest.utils.avg_stay_time import avg_stay_time
from invest.utils.tag_avg_stay_time import tag_avg_stay_time
from invest.utils.filtered_mean import filtered_mean
from invest.utils.bet_buy_ratio import bet_buy_ratio
from invest.utils.bet_sell_ratio import bet_sell_ratio
from invest.utils.avg_cash_ratio import avg_cash_ratio
from invest.utils.avg_trade_ratio import avg_trade_ratio, avg_buy_ratio, avg_sell_ratio
from invest.utils.date_filter import filter_date
from datetime import datetime, timedelta

def make_df_graph1(userId, filter: bool = False):
    # 평균 턴 체류시간, tag 발생 턴 평균 체류시간 + 우리아이 나이대 평균 값
    cols = ["investSessionId", 
            "userId",
            "turn", 
            "startedAt", 
            "endedAt",
            "newsTag"]
    df = load_invest_df(cols, "invest", False)

    if filter:
        filter_date(df)
    
    df1 =avg_stay_time(df)
    df1 = filtered_mean(df1, "avgStayTime", userId)

    df2 = tag_avg_stay_time(df)
    df2 = filtered_mean(df2, "tagAvgStayTime", userId)

    fin_df = pd.merge(df1, df2, on=["investSessionId", "userId"], how="inner")
    fin_df.drop(columns="investSessionId", inplace=True)

    return fin_df

def make_df_graph2_1(userId, filter: bool = False):
    # 종목별 구매 비율 영역 그래프
    cols = ["investSessionId", 
            "userId",
            "turn", 
            "riskLevel", 
            "numberOfShares", 
            "startedAt",
            "deltaShares"]
    df = load_invest_df(cols, "invest", False)

    if filter:
        filter_date(df)

    df = avg_buy_ratio(df)
    df = filtered_mean(df, ["highBuyRatio", "midBuyRatio", "lowBuyRatio"], userId)
   
    df.drop(columns="investSessionId", inplace=True)

    return df

def make_df_graph2_2(userId, filter: bool = False):
    # 종목별 판매 비율 영역 그래프
    cols = ["investSessionId", 
            "userId", 
            "turn", 
            "riskLevel", 
            "numberOfShares", 
            "startedAt",
            "deltaShares"]
    df = load_invest_df(cols, "invest", False)

    if filter:
        filter_date(df)
    
    df = avg_sell_ratio(df)
    df = filtered_mean(df, ["highSellRatio", "midSellRatio", "lowSellRatio"], userId)
    
    df.drop(columns="investSessionId", inplace=True)

    return df

def make_df_graph2_3(userId, filter: bool = False):
    # 종목별 판매/구매 비율 누적 막대 그래프 vs 우리아이 나이대 평균
    cols = ["investSessionId", 
            "userId", 
            "turn", 
            "riskLevel", 
            "numberOfShares", 
            "startedAt",
            "deltaShares"]
    df = load_invest_df(cols, "invest", False)

    if filter:
        filter_date(df)

    buy = avg_buy_ratio(df)
    sell = avg_sell_ratio(df)
    df = avg_trade_ratio(buy, sell)

    Sell = ["highSellRatio","midSellRatio","lowSellRatio"]
    Buy = ["highBuyRatio","midBuyRatio","lowBuyRatio"]

    all_types = [("Sell", Sell), ("Buy", Buy)]

    # 우리 아이랑 같은 나이를 갖는 행만 필터링
    age_series = df.loc[df["userId"] == userId, "age"]

    if age_series.empty:
        raise ValueError(f"userId '{userId}'에 해당하는 행이 없습니다.")

    child_age = age_series.iloc[0]
    # child_age = df.loc[df["userId"]==userId, "age"].iloc[0] 
    df = df[df["age"] == child_age].copy()
    for label, col_list in all_types:
        for col in col_list:
            # 우리아이 나이대 평균
            col_mean = df[f"{col}"].mean()
            new_col = col.replace(label, "")
            df[f'{new_col}_age'] = col_mean
        df['Type'] = label

    print(df.columns)
    
    # 우리아이 평균
    filtered_df = df[df["userId"] == userId]

    for label, col_list in all_types:
        for col in col_list:
            my_mean = filtered_df[f"{col}"].mean()
            new_col = col.replace(label, "")
            filtered_df[f'My{new_col}Mean'] = my_mean
        filtered_df['Type'] = label

    print(filtered_df.columns)

    # age drop
    filtered_df.drop(columns=["investSessionId", "age", "highSellRatio","midSellRatio","lowSellRatio", "highBuyRatio","midBuyRatio","lowBuyRatio"], inplace=True)
    
    return filtered_df

def make_df_graph3(userId, filter: bool = False):
    cols = ["investSessionId",
            "userId", 
            "turn",
            "newsTag",
            "riskLevel",
            "beforeValue",
            "currentValue",
            "numberOfShares",
            "startedAt", 
            "transactionType"]
    df = load_invest_df(cols, "invest", False)

    if filter:
        filter_date(df)

    df1 = bet_buy_ratio(df)
    df1 = filtered_mean(df1, "betBuyRatio", userId)

    df2 = bet_sell_ratio(df)
    df2 = filtered_mean(df2, "betSellRatio", userId)

    fin_df = pd.merge(df1, df2, on=["investSessionId", "userId"], how="outer")
    fin_df.drop(columns="investSessionId", inplace=True)

    return fin_df

def make_df_graph4(userId, filter: bool = False):
    cols = ['investSessionId', 
            'userId',
            'seedMoney',
            'chapterId',
            'turn',
            "startedAt",
            'currentPoint']
    df = load_invest_df(cols, "invest", True)

    if filter:
        filter_date(df)

    df = avg_cash_ratio(df)
    df = filtered_mean(df, "avgCashRatio", userId)
    df.drop(columns="investSessionId", inplace=True)

    return df