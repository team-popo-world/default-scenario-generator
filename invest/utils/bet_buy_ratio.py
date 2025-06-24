# 구매 배팅 성공률
# = tag 뉴스 발생 턴에서 해당 종목 구매 후 다음 턴에서 가격이 증가한 횟수 / 
# / tag 뉴스 발생 턴에서 해당 종목을 구매한 횟수
import pandas as pd

def bet_buy_ratio(df):
    # 구매 베팅 성공
    bet_win = df[["investSessionId",
                  "userId",
                  "age",
                  "turn",
                  "newsTag",
                  "riskLevel",
                  "beforeValue",
                  "currentValue", 
                  "transactionType",
                  "startedAt"]].copy()

    # 다음 턴의 value 컬럼 구하기
    bet_win.sort_values(by=["investSessionId","riskLevel","turn"], inplace=True)
    bet_win["nextValue"] = bet_win["currentValue"].shift(-1)

    # tag 뉴스 턴에서 해당 종목을 구매한 횟수
    bet_buy = bet_win.loc[(bet_win["newsTag"]==bet_win["riskLevel"]) & (bet_win["transactionType"]=="BUY")].copy()
    bet_buy_total = bet_buy.groupby("investSessionId")["nextValue"].count().reset_index().rename(columns={"nextValue":"bet_buy_total"})

    # tag 뉴스 턴에서 해당 종목을 구매하고 다음 턴에서 가격이 오른 횟수
    bet_buy["value_diff"] = bet_buy["nextValue"] - bet_buy["currentValue"]
    bet_buy_win = bet_buy[bet_buy["value_diff"]>0]
    bet_buy_win = bet_buy_win.groupby("investSessionId")["value_diff"].count().reset_index().rename(columns={"value_diff":"bet_buy_win"})

    # 성공 비율 계산
    bet_buy_df = pd.merge(bet_buy_total, bet_buy_win, on="investSessionId", how="left")
    bet_buy_df["betBuyRatio"] = bet_buy_df["bet_buy_win"] / bet_buy_df["bet_buy_total"]

    # nan값 0으로 채우기
    bet_buy_df = bet_buy_df.fillna(0) # 데이터가 없어서 nan으로 출력됨..! 0으로 채워주기기

    # 필요없는 컬럼 삭제
    bet_buy_df.drop(columns=["bet_buy_total","bet_buy_win"], inplace=True)

    # ✅ sessionId별 첫 turn 기준 startedAt 추출
    first_turn_info = bet_win.sort_values(by=["investSessionId", "turn"]).groupby("investSessionId").first().reset_index()
    user_info = first_turn_info[["investSessionId", "userId", "age", "startedAt"]]

    bet_buy_df = pd.merge(bet_buy_df, user_info, on="investSessionId", how="left")
    
    return bet_buy_df