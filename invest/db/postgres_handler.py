import os
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv(override=True)

# snake_case -> camelCase
def snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def load_postgres_data(query: str):
    host=os.getenv("DB_HOST")
    port=os.getenv("DB_PORT")
    dbname=os.getenv("DB_NAME")
    user=os.getenv("DB_USER")
    password=quote_plus(os.getenv("DB_PASSWORD"))

    engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    )

    df = pd.read_sql(query, engine)

    df.columns = [snake_to_camel(col) for col in df.columns]

    return df