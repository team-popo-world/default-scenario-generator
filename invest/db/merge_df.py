from invest.db.mongo_handler import load_mongo_data
from invest.db.postgres_handler import load_postgres_data

def load_invest_df(col: list = None, collection: str = "invest",  use_seed: bool = False):
    # MongoDB
    mongo_df = load_mongo_data(col, collection)

    # PostgreSQL
    seed_query = "SELECT chapter_id, seed_money FROM invest_chapter ;"
    user_query = "SELECT user_id, sex, age FROM users;"
    seed_df = load_postgres_data(seed_query)
    user_df = load_postgres_data(user_query)

    if use_seed:
        merge = mongo_df.merge(seed_df, on="chapterId", how="inner")
    else:
        merge = mongo_df.copy()

    ### user_df에 있는 userId가 uuid로 출력됨 -> str타입으로 바꿔서 출력
    user_df['userId'] = user_df['userId'].astype(str)

    merged_df = merge.merge(user_df, on="userId", how="inner")

    return merged_df

### 각 모듈의 출력값 ###
### investSessionId, userId, age, 각 집계값, startedAt은 필수로 나와야함 ###