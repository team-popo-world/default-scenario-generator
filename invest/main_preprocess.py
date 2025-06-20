from db.merge_df import load_df
from utils.trading_turn import trading_turn
from utils.transaction_num import transaction_num
from utils.avg_cash_ratio import avg_cash_ratio
from utils.avg_stay_time import avg_stay_time
from utils.avg_trade_ratio import avg_trade_ratio, avg_buy_ratio, avg_sell_ratio
from utils.tag_avg_stay_time import tag_avg_stay_time
from utils.bet_buy_ratio import bet_buy_ratio
from utils.bet_sell_ratio import bet_sell_ratio
from utils.bet_shares import bet_shares

df = load_df(None, "invest", True)
print(df.head())

# Preprocessing
userInfo = df[['userId', 'sex', 'age']].copy()
print("##########UserInfo##########", userInfo)

tradingTurn = trading_turn(df)
print("tradingTurn", tradingTurn.head())

transactionNum = transaction_num(df)
print("transactionNum", transactionNum.head())

# age 컬럼 있는 모듈 결과에서 age컬럼 제거
avgCashRatio = avg_cash_ratio(df)   # age 컬럼 제거
avgCashRatio = avgCashRatio.drop(columns="age")
print("avgCashRatio", avgCashRatio.head())

avgStayTime = avg_stay_time(df)   # age 컬럼 제거
avgStayTime = avgStayTime.drop(columns="age")
print("avgStayTime", avgStayTime.head())

buy = avg_buy_ratio(df)
sell = avg_sell_ratio(df)
avgTradeRatio = avg_trade_ratio(buy, sell)
print("avgTradeRatio", avgTradeRatio.head())

tagAvgStayTime = tag_avg_stay_time(df)   # age 컬럼 제거
tagAvgStayTime = tagAvgStayTime.drop(columns="age")
print("tagAvgStayTime", tagAvgStayTime.head())

betBuyRatio = bet_buy_ratio(df)
print("betBuyRatio", betBuyRatio.head())

betSellRatio = bet_sell_ratio(df)   # age 컬럼 제거
betSellRatio = betSellRatio.drop(columns="age")
print("betSellRatio", betSellRatio.head())

betShares = bet_shares(df)
print("betShares", betShares.head())

merged = tradingTurn.merge(transactionNum, on=['investSessionId', 'userId'], how='inner').merge(avgCashRatio, on=['investSessionId', 'userId'], how='inner').merge(avgStayTime, on=['investSessionId', 'userId'], how='inner').merge(avgTradeRatio, on=["investSessionId", "userId"], how='inner').merge(tagAvgStayTime, on=['investSessionId', 'userId'], how='inner').merge(betBuyRatio, on=['investSessionId', 'userId'], how='inner').merge(betSellRatio, on=['investSessionId', 'userId'], how='inner').merge(betShares, on=['investSessionId', 'userId'], how='inner')
print("####################################################################FINAL WITHOUT USER_DF####################################################################")
print(merged.head())

final_data = merged.merge(userInfo, on='userId', how="inner")
print("####################################################################FINAL DATA####################################################################")
print(final_data.head())

# rf_predict_invest_type(final_data)