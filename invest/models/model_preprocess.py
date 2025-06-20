import pandas as pd

#from models.preprocessing.userId_drop import userId_drop
from preprocessing.change_chapterId import change_chapterId
from preprocessing.label_encoder import label_encoder

def model_preprocess():

    # 데이터 불러오기
    df = pd.read_csv(".\data\invest_dummy.csv")

    #df = userId_drop(df1)

    # chpater 명 변경
    df = change_chapterId(df)

    # 레이블 인코딩
    encoding_cols = ["userId", "sex","chapterId", "investPro"]
    df, encoders_dict, label_mappings  = label_encoder(df, encoding_cols) # 인코더 객체, 인코딩 매핑


    # investSessionId 삭제
    df.drop("investSessionId", axis=1, inplace=True)

    
    # 결측치 확인
    #print(df.isna().sum())
    
    return df

