from sklearn.metrics import silhouette_score
import mlflow
import numpy as np
import pickle
import os



def result(df, model, cluster_labels, folder_path):
    # 평가 지표 계산
    silhouette_avg = silhouette_score(df, cluster_labels)
    inertia = model.inertia_
    
    # 각 클러스터의 크기 계산
    unique, counts = np.unique(cluster_labels, return_counts=True)
    cluster_sizes = dict(zip(unique, counts))
    
    # 메트릭 로깅
    mlflow.log_metric("silhouette_score", silhouette_avg)
    mlflow.log_metric("inertia", inertia)
    mlflow.log_metric("total_samples", len(df))
    
    # 각 클러스터 크기 로깅
    for cluster_id, size in cluster_sizes.items():
        mlflow.log_metric(f"cluster_{cluster_id}_size", size)
        mlflow.log_metric(f"cluster_{cluster_id}_percent", size/len(df))
    
    # 클러스터 중심점 저장
    centers_dict = {}
    for i, center in enumerate(model.cluster_centers_):
        centers_dict[f"cluster_{i}_center"] = center.tolist()
        mlflow.log_param(f"cluster_{i}_center_x", center[0]) # 중심점의 x좌표
        mlflow.log_param(f"cluster_{i}_center_y", center[1]) # 중심점의 y좌표
    
    # 추가 정보 저장
    cluster_info = {
        'silhouette_score': silhouette_avg,
        'inertia': inertia,
        'cluster_centers': model.cluster_centers_.tolist(),
        'cluster_sizes': cluster_sizes,
        'labels': cluster_labels.tolist()
    }

    # 클러스터 정보를 pickle 파일로 저장
    cluster_info_path = folder_path / "cluster_info.pkl"

    with open(str(cluster_info_path), "wb") as f:
        pickle.dump(cluster_info, f)
    mlflow.log_artifact(str(cluster_info_path))
    
    # 파일정리 (MLflow 업로드 후 로컬 파일 삭제)
    if os.path.exists(cluster_info_path):  # 수정: 전체 경로 사용
        os.remove(cluster_info_path)
        
    
    return silhouette_avg, inertia, cluster_sizes

