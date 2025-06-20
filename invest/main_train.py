import mlflow
import pandas as pd
from main_preprocess import model_preprocess
from sklearn.model_selection import train_test_split
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# 모델 성능 추적: mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.sklearn.autolog() # sklearn 모델 빌드에 대한 로그 기록



# 데이터 불러오기 + 전처리
df = model_preprocess()


# 모델 생성
#clf = DecisionTreeClassifier(random_state=42)


# 모델 훈련


# 예측


# 예측 결과 출력
