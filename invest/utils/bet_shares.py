# 위험 감수율 #
# betMidShares: 중위험 tag 발생 시 중위험 종목 구매 수량
# betHighShares: 고위험 tag 발생 시 중위험 종목 구매 수량
import pandas as pd

def bet_shares(df):
    bet_data = df[["investSessionId", 
                   "userId", 
                   "turn",
                   "newsTag",
                   "riskLevel",
                   "numberOfShares",
                   "deltaShares", 
                   "transactionType", 
                   "beforeValue",
                   "currentValue",
                   "income"]].copy()

    # newsTag 발생 시 해당 종목을 구매한 경우
    bet_buy = bet_data.loc[(bet_data["newsTag"] == bet_data["riskLevel"]) & (bet_data["transactionType"]=="BUY")]

    bet_mid = bet_buy[bet_buy["riskLevel"]=="mid"].groupby(["investSessionId", "userId"])["deltaShares"].sum().reset_index().rename(columns={"deltaShares":"betMidShares"})
    bet_high = bet_buy[bet_buy["riskLevel"]=="high"].groupby(["investSessionId", "userId"])["deltaShares"].sum().reset_index().rename(columns={"deltaShares":"betHighShares"})

    risk_taking = pd.merge(bet_mid, bet_high, on=["investSessionId", "userId"], how="outer")

    # nan 인 값들은 0으로 채우기
    risk_taking = risk_taking.fillna(0)

    return risk_taking

