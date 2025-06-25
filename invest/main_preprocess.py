import pandas as pd

from db.mongo_handler import load_mongo_data
from db.postgres_handler import load_postgres_data

# from utils.trading_turn import trading_turn
# from utils.transaction_num import transaction_num
# from utils.avg_cash_ratio import avg_cash_ratio
# from utils.avg_stay_time import avg_stay_time
# from utils.avg_trade_ratio import avg_trade_ratio, avg_buy_ratio, avg_sell_ratio
# from utils.tag_avg_stay_time import tag_avg_stay_time
# from utils.bet_buy_ratio import bet_buy_ratio
# from utils.bet_sell_ratio import bet_sell_ratio
# from utils.bet_shares import bet_shares

# from models.preprocessing.delete_cols import delete_cols
# from models.preprocessing.time_type import time_type
# from models.preprocessing.encoder import one_hot_encoder
# from models.preprocessing.scaler import standard_scaler

# airflow 용 import
from invest.db.mongo_handler import load_mongo_data
from invest.db.postgres_handler import load_postgres_data

from invest.utils.trading_turn import trading_turn
from invest.utils.transaction_num import transaction_num
from invest.utils.avg_cash_ratio import avg_cash_ratio
from invest.utils.avg_stay_time import avg_stay_time
from invest.utils.avg_trade_ratio import avg_trade_ratio, avg_buy_ratio, avg_sell_ratio
from invest.utils.tag_avg_stay_time import tag_avg_stay_time
from invest.utils.bet_buy_ratio import bet_buy_ratio
from invest.utils.bet_sell_ratio import bet_sell_ratio
from invest.utils.bet_shares import bet_shares

from invest.models.preprocessing.delete_cols import delete_cols
from invest.models.preprocessing.time_type import time_type
from invest.models.preprocessing.encoder import one_hot_encoder
from invest.models.preprocessing.scaler import standard_scaler


def model_preprocess():
    # 데이터 불러오기
    mongo_df = load_mongo_data(None, "invest")

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

    # 사용자 정보, 시나리오 정보
    userInfo = df[['userId', 'sex', 'age', 'createdAt']].drop_duplicates()
    scenarioInfo = df[["chapterId","investSessionId"]].drop_duplicates()

    # 집계
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

    # userId, scenarioId drop
    df = fin_df.drop("userId", axis=1)

    # 시간 타입 데이터 변환
    df_time = time_type(df)

    # 성별 원핫인코딩
    df_encoded = one_hot_encoder(df_time, ['sex', 'chapterId'])

    # 데이터 표준화
    df_scaled = standard_scaler(df_encoded)

    # userId 다시 붙여넣기
    df_scaled["userId"] = fin_df["userId"].values

    return df_scaled

