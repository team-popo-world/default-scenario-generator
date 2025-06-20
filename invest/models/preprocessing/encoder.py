import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# 입력한 컬럼에 대해 레이블 인코딩

def label_encoder(df, cols):
    """
    주어진 DataFrame의 컬럼들을 레이블 인코딩하고,
    각 컬럼에 사용된 LabelEncoder 객체와 매핑 정보를 반환합니다.

    Args:
        df (pd.DataFrame): 레이블 인코딩할 DataFrame.
        cols (list): 레이블 인코딩할 컬럼 이름 리스트.

    Returns:
        tuple:
            - pd.DataFrame: 레이블 인코딩된 DataFrame.
            - dict: {컬럼명: LabelEncoder 객체} 형태의 딕셔너리.
            - dict: {컬럼명: {원본값: 인코딩값}} 형태의 매핑 정보 딕셔너리.
    """
    encoders_dict = {}     # {컬럼명: LabelEncoder 객체}
    label_mappings = {}    # {컬럼명: {원본값: 인코딩값}}

    df_encoded = df.copy() # 원본 DataFrame을 변경하지 않기 위해 복사

    for col in cols:
        if col not in df_encoded.columns:
            print(f"경고: 컬럼 '{col}'이(가) DataFrame에 존재하지 않습니다.")
            continue

        # LabelEncoder 객체 생성
        encoder = LabelEncoder()

        # 컬럼 인코딩 및 변경된 값으로 업데이트
        # fit_transform은 인코딩과 학습을 동시에 수행
        df_encoded[col] = encoder.fit_transform(df_encoded[col])

        # encoder 객체 저장
        encoders_dict[col] = encoder # 컬럼 이름을 키로 사용하여 객체 저장

        # 레이블 매핑 정보 저장
        # encoder.classes_는 원본 값들, encoder.transform(encoder.classes_)는 인코딩된 값들
        label_mappings[col] = {original_label: encoded_value
                               for original_label, encoded_value in zip(encoder.classes_, encoder.transform(encoder.classes_))}
    
    return df_encoded, encoders_dict, label_mappings



def one_hot_encoder(df, cols):
    
    df_encoded = pd.get_dummies(
        df, 
        columns=cols,
        drop_first=True,
        dtype=int
    )

    print(f"원본 컬럼 수: {df.shape[1]}")
    print(f"인코딩 후 컬럼 수: {df_encoded.shape[1]}")
    print(f"추가된 컬럼 수: {df_encoded.shape[1] - df.shape[1]}")
    
    return df_encoded



