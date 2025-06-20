import pandas as pd

def userId_drop(df):
    df_copy = df_copy()
    df_copy.drop("userId", axis=1, inplace=True)
    return df_copy
