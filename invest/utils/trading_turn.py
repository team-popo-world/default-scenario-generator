# 거래참여 턴 개수
def trading_turn(df):
    tpt = df[['investSessionId', 
          'userId',
          'turn',
          'riskLevel',
          'transactionType']].copy()
    
    hold_flags = tpt.groupby(['investSessionId', 'userId', 'turn'])['transactionType'].apply(lambda x: int((x != "KEEP").any())).reset_index(name="notAllKeep")
    tradingTurn = hold_flags.groupby(['investSessionId', 'userId'])['notAllKeep'].mean().reset_index(name="avgNotKeep")
    
    return tradingTurn