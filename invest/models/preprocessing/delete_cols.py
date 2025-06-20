import pandas as pd

# 컬럼에 age, startedAt이 포함되어있으면 삭제

def delete_cols(df):
    if df is None:
        print("DataFrame이 None입니다.")
        return None
    
    if df.empty:
        print("DataFrame이 비어있습니다.")
        return df
    
    # 삭제할 컬럼 리스트
    cols_to_drop = ['age', 'startedAt']
    
    # 존재하는 컬럼만 필터링
    existing_cols = [col for col in cols_to_drop if col in df.columns]
    
    if existing_cols:
        df_cleaned = df.drop(columns=existing_cols)
        print(f"삭제된 컬럼: {existing_cols}")
        print(f"남은 컬럼: {list(df_cleaned.columns)}")
        return df_cleaned
    else:
        print("삭제할 컬럼이 데이터프레임에 존재하지 않습니다.")
        return df