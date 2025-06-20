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
from models.preprocessing.label_encoder import label_encoder

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
# Preprocessing
userInfo = df[['userId', 'sex', 'age', 'createdAt']].drop_duplicates()
scenarioInfo = mongo_df[["scenarioId", "investSessionId"]].drop_duplicates()

tradingTurn = trading_turn(df)

transactionNum = transaction_num(df)

# age, startedAt 컬럼 있는 모듈 결과에서 age컬럼 제거
avgCashRatio = avg_cash_ratio(df)
avgCashRatio = avgCashRatio.drop(["age","startedAt"], axis=1)

avgStayTime = avg_stay_time(df)
avgStayTime = avgStayTime.drop(["age","startedAt"], axis=1)

buy = avg_buy_ratio(df)
sell = avg_sell_ratio(df)
avgTradeRatio = avg_trade_ratio(buy, sell)

tagAvgStayTime = tag_avg_stay_time(df)
tagAvgStayTime = tagAvgStayTime.drop(["age"], axis=1)

betBuyRatio = bet_buy_ratio(df)

betSellRatio = bet_sell_ratio(df)
betSellRatio = betSellRatio.drop(["age"], axis=1)

betShares = bet_shares(df)

merged = tradingTurn.merge(transactionNum, on=['investSessionId', 'userId'], how='inner').merge(avgCashRatio, on=['investSessionId', 'userId'], how='inner').merge(avgStayTime, on=['investSessionId', 'userId'], how='inner').merge(avgTradeRatio, on=["investSessionId", "userId"], how='inner').merge(tagAvgStayTime, on=['investSessionId', 'userId'], how='inner').merge(betBuyRatio, on=['investSessionId', 'userId'], how='inner').merge(betSellRatio, on=['investSessionId', 'userId'], how='inner').merge(betShares, on=['investSessionId', 'userId'], how='inner')

merged2 = merged.merge(userInfo, on='userId', how="inner")

fin_df = merged2.merge(scenarioInfo, on="investSessionId", how="inner")

# investSessionId drop
df = fin_df.drop("investSessionId", axis=1)

# 레이블 인코딩
df = label_encoder(fin_df, ["userId",""])
print(df)