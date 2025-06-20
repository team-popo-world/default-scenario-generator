import pandas as pd

def change_chapterId(df):

    df_copy = df.copy()

    # 매핑 딕셔너리
    chapter_id_mapping = {
    'chapter1': "1111",
    'chapter2': "2222",
    'chapter3': "3333",
    'chapter4': "4444"
    }
    
    df_copy['chapterId'] = df_copy['chapterId'].map(chapter_id_mapping)
    
    return df_copy