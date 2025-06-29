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

def make_avg_stay_time(userId, filter: bool = False):
    try:
        # 필요한 컬럼 정의
        cols = ["investSessionId", 
                "userId",
                "turn", 
                "startedAt", 
                "endedAt",
                "newsTag"]
        
        # 데이터 로드
        df = load_invest_df(cols, "invest", False)
        if df.empty:
            return pd.DataFrame()

        # 필터링
        if filter:
            df = filter_date(df)
        if df.empty:
            return pd.DataFrame()

        # 평균 체류시간 계산
        df1 = avg_stay_time(df)
        if df1.empty:
            return pd.DataFrame()
        df1 = filtered_mean(df1, "avgStayTime", userId)
        if df1.empty:
            return pd.DataFrame()

        # 태그 평균 체류시간 계산
        df2 = tag_avg_stay_time(df)
        if df2.empty:
            return pd.DataFrame()
        df2 = filtered_mean(df2, "tagAvgStayTime", userId)
        if df2.empty:
            return pd.DataFrame()

        # 병합
        fin_df = pd.merge(df1, df2, on=["investSessionId", "userId"], how="inner")
        if fin_df.empty:
            return pd.DataFrame()

        # 필요없는 컬럼 제거
        fin_df.drop(columns="investSessionId", inplace=True, errors="ignore")

        return fin_df

    except Exception as e:
        print(f"[ERROR] make_avg_stay_time failed for userId {userId}: {e}")
        return pd.DataFrame()

def make_buy_ratio(userId, filter: bool = False):
    try:
        # 필요한 컬럼 정의
        cols = ["investSessionId", 
                "userId",
                "turn", 
                "riskLevel", 
                "numberOfShares", 
                "startedAt",
                "deltaShares"]
        
        # 데이터 로드
        df = load_invest_df(cols, "invest", False)
        if df.empty:
            return pd.DataFrame()

        # 필터 적용
        if filter:
            df = filter_date(df)
        if df.empty:
            return pd.DataFrame()

        # 평균 구매 비율 계산
        df = avg_buy_ratio(df)
        if df.empty:
            return pd.DataFrame()

        df = filtered_mean(df, ["highBuyRatio", "midBuyRatio", "lowBuyRatio"], userId)
        if df.empty:
            return pd.DataFrame()

        # 불필요한 컬럼 제거
        df.drop(columns="investSessionId", inplace=True, errors="ignore")

        return df

    except Exception as e:
        print(f"[ERROR] make_buy_ratio failed for userId {userId}: {e}")
        return pd.DataFrame()

def make_sell_ratio(userId, filter: bool = False):
    try:
        # 필요한 컬럼 정의
        cols = ["investSessionId", 
                "userId", 
                "turn", 
                "riskLevel", 
                "numberOfShares", 
                "startedAt",
                "deltaShares"]
        
        # 데이터 로드
        df = load_invest_df(cols, "invest", False)
        if df.empty:
            return pd.DataFrame()

        # 필터 적용
        if filter:
            df = filter_date(df)
        if df.empty:
            return pd.DataFrame()

        # 평균 판매 비율 계산
        df = avg_sell_ratio(df)
        if df.empty:
            return pd.DataFrame()

        df = filtered_mean(df, ["highSellRatio", "midSellRatio", "lowSellRatio"], userId)
        if df.empty:
            return pd.DataFrame()

        # 불필요한 컬럼 제거
        df.drop(columns="investSessionId", inplace=True, errors="ignore")

        return df

    except Exception as e:
        print(f"[ERROR] make_sell_ratio failed for userId {userId}: {e}")
        return pd.DataFrame()

def make_buy_sell_ratio(userId, filter: bool = False):
    try:
        # 필요한 컬럼
        cols = ["investSessionId", 
                "userId", 
                "turn", 
                "riskLevel", 
                "numberOfShares", 
                "startedAt",
                "deltaShares"]
        
        df = load_invest_df(cols, "invest", False)
        if df.empty:
            return pd.DataFrame()

        if filter:
            df = filter_date(df)
        if df.empty:
            return pd.DataFrame()

        buy = avg_buy_ratio(df)
        sell = avg_sell_ratio(df)
        if buy.empty or sell.empty:
            return pd.DataFrame()

        df = avg_trade_ratio(buy, sell)
        if df.empty:
            return pd.DataFrame()

        Sell = ["highSellRatio", "midSellRatio", "lowSellRatio"]
        Buy = ["highBuyRatio", "midBuyRatio", "lowBuyRatio"]
        all_types = [("Sell", Sell), ("Buy", Buy)]

        # userId로 나이 필터링
        age_series = df.loc[df["userId"] == userId, "age"]
        if age_series.empty:
            return pd.DataFrame()

        child_age = age_series.iloc[0]
        df = df[df["age"] == child_age].copy()
        if df.empty:
            return pd.DataFrame()

        for label, col_list in all_types:
            for col in col_list:
                col_mean = df[col].mean()
                new_col = col.replace(label, "")
                df[f'{new_col}_age'] = col_mean
            df['Type'] = label

        filtered_df = df[df["userId"] == userId].copy()
        if filtered_df.empty:
            return pd.DataFrame()

        for label, col_list in all_types:
            for col in col_list:
                my_mean = filtered_df[col].mean()
                new_col = col.replace(label, "")
                filtered_df[f'My{new_col}Mean'] = my_mean
            filtered_df['Type'] = label

        filtered_df.drop(columns=[
            "investSessionId", "age", 
            "highSellRatio", "midSellRatio", "lowSellRatio", 
            "highBuyRatio", "midBuyRatio", "lowBuyRatio", "startedAt"
        ], inplace=True, errors="ignore")

        return filtered_df

    except Exception as e:
        print(f"[ERROR] make_buy_sell_ratio failed for userId {userId}: {e}")
        return pd.DataFrame()

def make_bet_ratio(userId, filter: bool = False):
    try:
        cols = [
            "investSessionId", "userId", "turn", "newsTag", "riskLevel", "age"
            "beforeValue", "currentValue", "numberOfShares", "startedAt", "transactionType"
        ]
        
        df = load_invest_df(cols, "invest", False)
        if df.empty:
            return pd.DataFrame()

        if filter:
            df = filter_date(df)
        if df.empty:
            return pd.DataFrame()

        df1 = bet_buy_ratio(df)
        if df1.empty:
            df1 = pd.DataFrame()
        
        if "age" in df1.columns:
            df1 = filtered_mean(df1, "betBuyRatio", userId)
        if df1.empty:
            df1 = pd.DataFrame()

        df2 = bet_sell_ratio(df)
        if df2.empty:
            df2 = pd.DataFrame()

        if "age" in df2.columns:
            df2 = filtered_mean(df2, "betSellRatio", userId)
        if df2.empty:
            df2 = pd.DataFrame()

        # 🔸 둘 다 비어있지 않은 경우에만 merge
        if not df1.empty and not df2.empty:
            fin_df = pd.merge(df1, df2, on=["investSessionId", "userId"], how="outer")
            fin_df.drop(columns="investSessionId", inplace=True, errors="ignore")
            
            # 👉 NaN/NaT/string 변환 추가
            fin_df = fin_df.fillna("")
            if "startedAt" in fin_df.columns:
                fin_df["startedAt"] = fin_df["startedAt"].astype(str)
            fin_df["userId"] = fin_df["userId"].astype(str)
            
            return fin_df
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"[ERROR] make_bet_ratio failed for userId {userId}: {e}")
        return pd.DataFrame()

def make_avg_cash_ratio(userId, filter: bool = False):
    try:
        cols = ['investSessionId', 
                'userId',
                'seedMoney',
                'chapterId',
                'turn',
                "startedAt",
                'currentPoint']
        
        df = load_invest_df(cols, "invest", True)
        if df.empty:
            return pd.DataFrame()

        if filter:
            df = filter_date(df)
        if df.empty:
            return pd.DataFrame()

        df = avg_cash_ratio(df)
        if df.empty:
            return pd.DataFrame()

        df = filtered_mean(df, "avgCashRatio", userId)
        if df.empty:
            return pd.DataFrame()

        df.drop(columns="investSessionId", inplace=True, errors="ignore")

        return df
    
    except Exception as e:
        print(f"[ERROR] make_avg_cash_ratio failed for userId {userId}: {e}")
        return pd.DataFrame()


def make_invest_style(userId, filter: bool = False):
    
    def load_cluster_data(fields=None):
        import os
        import pandas as pd
        from pymongo import MongoClient
        from dotenv import load_dotenv

        load_dotenv(override=True)

        # MongoDB 연결 정보
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB_NAME")
        collection_name = "invest_cluster_result"

        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]

        # fields 리스트를 projection 딕셔너리로 변환
        projection = {field: 1 for field in fields} if fields else None
        if projection is not None:
            projection['_id'] = 0  # 기본적으로 _id는 제외

        df = pd.DataFrame(list(collection.find({}, projection)))

        return df
    
    try:
        df = load_cluster_data(None)
        if df.empty:
            return pd.DataFrame()

        if filter:
            df = filter_date(df)
        if df.empty:
            return pd.DataFrame()

        filtered_df = df[df["user_id"]==userId]

        if filtered_df.empty:
            return pd.DataFrame()

        result_df = filtered_df["cluster_num"].value_counts().reset_index()
        
        if result_df.empty:
            return pd.DataFrame()

        return result_df

    except Exception as e:
        print(f"[ERROR] make_avg_cash_ratio failed for userId {userId}: {e}")
        return pd.DataFrame()
    