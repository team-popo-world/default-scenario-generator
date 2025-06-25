from sklearn.cluster import KMeans


def kmeans(df, n_clusters, init_method, max_iter, n_init, random_state):
    
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

    # 원본 데이터프레임에 클러스터 라벨 추가
    X_features['cluster_num'] = cluster_labels


    return kmeans, cluster_labels, X_features