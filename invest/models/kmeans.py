from sklearn.cluster import KMeans
import mlflow
from mlflow.models import infer_signature
import numpy as np


def kmeans(df, n_clusters, init_method, max_iter, n_init, random_state):
    
    # 파라미터 로깅
    mlflow.log_param("n_clusters", n_clusters)
    mlflow.log_param("init_method", init_method)
    mlflow.log_param("max_iter", max_iter)
    mlflow.log_param("n_init", n_init)
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("data_shape", df.shape)

    X_features = df.copy()

    # K-means 모델 학습
    kmeans = KMeans(
        n_clusters=n_clusters,
        init=init_method,
        max_iter=max_iter,
        n_init=n_init,
        random_state=random_state
    )
    
    cluster_labels = kmeans.fit_predict(X_features)

    # 시그니처 추론 (원본 피처 -> 클러스터 레이블)
    signature = infer_signature(X_features, cluster_labels)

    # 원본 데이터프레임에 클러스터 라벨 추가
    X_features['cluster_num'] = cluster_labels

    # 모델 로깅
    mlflow.sklearn.log_model(
        kmeans, 
        name="clustering_model",
        signature=signature,
        input_example=X_features[:5]
    )

    return kmeans, cluster_labels, X_features