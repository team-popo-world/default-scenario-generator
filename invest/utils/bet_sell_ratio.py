# 판매 배팅 성공률
# = tag 뉴스 발생 턴에서 해당 종목 판매 후 다음 턴에서 가격이 감소한 횟수 
# / tag 뉴스 발생 턴에서 해당 종목을 판매한 횟수
import pandas as pd

def bet_sell_ratio(df):
    # 판매 베팅 성공
    bet_win = df[["investSessionId",
                  "userId",
                  "age",
                  "turn",
                  "newsTag",
                  "riskLevel",
                  "beforeValue",
                  "currentValue", 
                  "transactionType"]].copy()

    # 다음 턴의 value 컬럼 구하기
    bet_win.sort_values(by=["investSessionId","riskLevel","turn"], inplace=True)
    bet_win["nextValue"] = bet_win.groupby(["investSessionId", "riskLevel"])["currentValue"].shift(-1)

    # tag 뉴스 턴에서 해당 종목을 판매한 횟수
    bet_sell = bet_win.loc[(bet_win["newsTag"]==bet_win["riskLevel"]) & (bet_win["transactionType"]=="SELL")].copy()
    bet_sell_total = bet_sell.groupby("investSessionId")["nextValue"].count().reset_index().rename(columns={"nextValue":"bet_sell_total"})

    # tag 뉴스 턴에서 해당 종목을 구매하고 다음 턴에서 가격이 오른 횟수
    bet_sell["value_diff"] = bet_sell["nextValue"] - bet_sell["currentValue"]
    bet_sell_win = bet_sell[bet_sell["value_diff"]<0]
    bet_sell_win = bet_sell_win.groupby("investSessionId")["value_diff"].count().reset_index().rename(columns={"value_diff":"bet_sell_win"})


    # 성공 비율 계산
    bet_sell_df = pd.merge(bet_sell_total, bet_sell_win, on="investSessionId", how="left")
    bet_sell_df["betSellRatio"] = bet_sell_df["bet_sell_win"] / bet_sell_df["bet_sell_total"]

    # nan값 0으로 채우기
    bet_sell_df = bet_sell_df.fillna(0) # 데이터가 없어서 nan으로 출력됨..! 0으로 채워주기기

    # 필요없는 컬럼 삭제
    bet_sell_df.drop(columns=["bet_sell_total","bet_sell_win"], inplace=True)

    first_turn_info = bet_win.sort_values(by=["investSessionId", "turn"]).groupby("investSessionId").first().reset_index()
    user_info = first_turn_info[["investSessionId", "userId", "age"]]

    bet_sell_df = pd.merge(bet_sell_df, user_info, on="investSessionId", how="left")
    
    return bet_sell_df
