# 거래 횟수
def transaction_num(df):
    nt = df[['investSessionId',
            'userId', 
            'turn',
            'riskLevel',
            'plusClick',
            'minusClick']].copy()

    nt['click'] = nt['plusClick'] + nt['minusClick']
    transactionNum = nt.groupby(['investSessionId', 'userId'])[['click']].mean().reset_index()

    return transactionNum