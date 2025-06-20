import pandas as pd

from db.mongo_handler import load_mongo_data
from db.postgres_handler import load_postgres_data

from utils.trading_turn import trading_turn
from utils.transaction_num import transaction_num
from utils.avg_cash_ratio import avg_cash_ratio
from utils.avg_stay_time import avg_stay_time
from utils.avg_trade_ratio import avg_trade_ratio, avg_buy_ratio, avg_sell_ratio
from utils.tag_avg_stay_time import tag_avg_stay_time
from utils.bet_buy_ratio import bet_buy_ratio
from utils.bet_sell_ratio import bet_sell_ratio
from utils.bet_shares import bet_shares

#from models.preprocessing.userId_drop import userId_drop
from models.preprocessing.delete_cols import delete_cols
from models.preprocessing.time_type import time_type
from models.preprocessing.encoder import one_hot_encoder
from models.preprocessing.scaler import standard_scaler



def model_preprocess():
    # 데이터 불러오기
    mongo_df = load_mongo_data(None, "invest_dummy")

    seed_query = "SELECT chapter_id, seed_money FROM invest_chapter ;"
    user_query = "SELECT user_id, sex, age, created_at FROM users;"
    #scenario_query = "SELECT investSessionId, scenarioId FROM invest_session;"

    seed_df = load_postgres_data(seed_query)
    user_df = load_postgres_data(user_query)
    #scenario_df = load_postgres_data(scenario_query)

    ### user_df에 있는 userId가 uuid로 출력됨 -> str타입으로 바꿔서 출력
    user_df['userId'] = user_df['userId'].astype(str)


    # 데이터 병합
    merged = mongo_df.merge(seed_df, on="chapterId", how="inner")
    df = merged.merge(user_df, on="userId", how="inner")


    # 집계
    userInfo = df[['userId', 'sex', 'age', 'createdAt']].drop_duplicates()
    scenarioInfo = df[["scenarioId", "chapterId","investSessionId"]].drop_duplicates()

    tradingTurn = trading_turn(df)
    transactionNum = transaction_num(df)
    avgCashRatio = avg_cash_ratio(df)
    avgStayTime = avg_stay_time(df)

    buy = avg_buy_ratio(df)
    sell = avg_sell_ratio(df)
    avgTradeRatio = avg_trade_ratio(buy, sell)

    tagAvgStayTime = tag_avg_stay_time(df)
    betBuyRatio = bet_buy_ratio(df)
    betSellRatio = bet_sell_ratio(df)
    betShares = bet_shares(df)

    # age, startedAt drop
    df_list = [tradingTurn, transactionNum, avgCashRatio, avgStayTime, avgTradeRatio, tagAvgStayTime, betBuyRatio, betSellRatio, betShares]

    for i in range(len(df_list)):
        df_list[i] = delete_cols(df_list[i])

    tradingTurn, transactionNum, avgCashRatio, avgStayTime, avgTradeRatio, tagAvgStayTime, betBuyRatio, betSellRatio, betShares = df_list


    # 데이터 병합
    merged = tradingTurn.merge(transactionNum, on=['investSessionId', 'userId'], how='inner').merge(avgCashRatio, on=['investSessionId', 'userId'], how='inner').merge(avgStayTime, on=['investSessionId', 'userId'], how='inner').merge(avgTradeRatio, on=["investSessionId", "userId"], how='inner').merge(tagAvgStayTime, on=['investSessionId', 'userId'], how='inner').merge(betBuyRatio, on=['investSessionId', 'userId'], how='inner').merge(betSellRatio, on=['investSessionId', 'userId'], how='inner').merge(betShares, on=['investSessionId', 'userId'], how='inner')
    merged2 = merged.merge(userInfo, on='userId', how="inner")
    fin_df = merged2.merge(scenarioInfo, on="investSessionId", how="inner")


    # 전처리

    # investSessionId를 index로
    fin_df = fin_df.set_index("investSessionId")

    # userId, scenarioId drop
    fin_df.drop(["userId","scenarioId"], axis=1, inplace=True)

    # 시간 타입 데이터 변환
    df = time_type(fin_df)

    # 성별 원핫인코딩
    df = one_hot_encoder(df, ['sex'])

    # 데이터 표준화
    df = standard_scaler(df)

    return df



df = model_preprocess()
print(df.head())
