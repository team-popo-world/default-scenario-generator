from invest.db.mongo_handler import load_mongo_data
from invest.db.postgres_handler import load_postgres_data

def load_invest_df(col: list = None, collection: str = "invest",  use_seed: bool = False):
    # MongoDB
    print(col)
    mongo_df = load_mongo_data(col, collection)
    print("laod_df내부에 있는 mongo_db", mongo_df.head())

    # PostgreSQL
    seed_query = "SELECT chapter_id, seed_money FROM invest_chapter ;"
    user_query = "SELECT user_id, sex, age FROM users;"
    seed_df = load_postgres_data(seed_query)
    user_df = load_postgres_data(user_query)
    print("laod_df내부에 있는 seed_df", seed_df.head())
    print("laod_df내부에 있는 user_df", user_df.head())

    if use_seed:
        merge = mongo_df.merge(seed_df, on="chapterId", how="inner")
    else:
        merge = mongo_df.copy()

    print("laod_df내부에 있는 seed + mongo", merge.head())

    ### user_df에 있는 userId가 uuid로 출력됨 -> str타입으로 바꿔서 출력
    user_df['userId'] = user_df['userId'].astype(str)

    print("🔍 merge 컬럼 목록:", merge.columns)
    print("🔍 user_df 컬럼 목록:", user_df.columns)

    merged_df = merge.merge(user_df, on="userId", how="inner")
    print("load_df내부에 있는 최종 merge_df", merged_df.head())

    return merged_df

### 각 모듈의 출력값 ###
### investSessionId, userId, age, 각 집계값, startedAt은 필수로 나와야함 ###