from sklearn.metrics import silhouette_score
import numpy as np
import pickle


def result(df, model, cluster_labels, folder_path):
    # 평가 지표 계산
    silhouette_avg = silhouette_score(df, cluster_labels)
    inertia = model.inertia_
    
    # 각 클러스터의 크기 계산
    unique, counts = np.unique(cluster_labels, return_counts=True)
    cluster_sizes = dict(zip(unique, counts))
    
    # 클러스터 중심점 정보
    cluster_centers = model.cluster_centers_
    
    # 추가 정보 저장
    cluster_info = {
        'silhouette_score': silhouette_avg,
        'inertia': inertia,
        'cluster_centers': cluster_centers.tolist(),
        'cluster_sizes': cluster_sizes,
        'labels': cluster_labels.tolist()
    }

    # 클러스터 정보를 pickle 파일로 저장 (로컬에만)
    cluster_info_path = folder_path / "cluster_info.pkl"
    with open(str(cluster_info_path), "wb") as f:
        pickle.dump(cluster_info, f)
    
    # 반환값에 필요한 정보들 추가
    return silhouette_avg, inertia, cluster_sizes, cluster_centers, cluster_info_path

