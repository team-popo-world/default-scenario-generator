import mlflow
import pandas as pd
from model_preprocess import model_preprocess
from sklearn.model_selection import train_test_split
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# 모델 성능 추적: mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.sklearn.autolog() # sklearn 모델 빌드에 대한 로그 기록



# 데이터 불러오기 + 전처리
df = model_preprocess()


# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    df.drop(["investPro"], axis=1),
    df['investPro'],
    random_state=42
)


# 모델 생성
#clf = DecisionTreeClassifier(random_state=42)
clf = RandomForestClassifier(
    n_estimators=100,        # 트리 개수
    max_depth=None,          # 최대 깊이 (제한 없음)
    random_state=42,         # 재현성을 위한 시드
    n_jobs=-1               # 모든 CPU 코어 사용
)

# 모델 훈련
clf = clf.fit(X_train, y_train)

# 예측
y_pred = clf.predict(X_test)

# 예측 결과 출력
print(y_pred)