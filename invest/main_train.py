import mlflow
import mlflow.sklearn
from invest.mlflow_config import get_mlflow_client
import numpy as np
from pathlib import Path
import pandas as pd
import os


# from models.kmeans import kmeans
# from models.result import result
# from models.feature_pairs import feature_pairs

# airflow 용 import
from invest.models.kmeans import kmeans
from invest.models.result import result
from invest.models.feature_pairs import feature_pairs



def model_train(with_id_df):
    # MLflow 설정 - mlflow_config.py 사용
    mlflow = get_mlflow_client()
    
    # investSessionId drop : 모델링용 데이터
    df = with_id_df.drop(["userId", "investSessionId"], axis=1)

    # 현재 스크립트 파일의 디렉토리 가져오기
    current_script_dir = Path(__file__).parent.resolve()
    
    # 시각화.png, 모델 결과.pkl 저장경로 지정 (현재 스크립트 위치 기준)
    folder_path = current_script_dir / 'models'

    # mlflow 실험 이름 설정
    experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'invest_model_training')

    # mlflow 실행 이름 설정
    run_name=f"kmeans_clustering_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
    
    with mlflow.start_run(run_name=run_name):
        # 1. 데이터 정보 로깅
        mlflow.log_params({
            'data_shape': f"{df.shape[0]}x{df.shape[1]}",
            'feature_count': df.shape[1],
            'sample_count': df.shape[0],
            'feature_names': list(df.columns)
        })

        # K-means 모델 파라미터 설정
        n_clusters = 5
        init_method = 'k-means++'
        max_iter = 300
        n_init = 10
        random_state = 42

        # 2. 하이퍼파라미터 로깅
        mlflow.log_params({
            'n_clusters': n_clusters,
            'init_method': init_method,
            'max_iter': max_iter,
            'n_init': n_init,
            'random_state': random_state,
            'algorithm': 'K-means'
        })
        
        # 모델 학습 및 예측
        model, cluster_labels, clustered_df = kmeans(df, n_clusters, init_method, max_iter, n_init, random_state)

        # 모델 평가 
        silhouette_avg, inertia, cluster_sizes, cluster_centers, cluster_info_path = result(df, model, cluster_labels, folder_path)
        
        # 3. 메트릭 로깅
        mlflow.log_metrics({
            'silhouette_score': silhouette_avg,
            'inertia': inertia,
            'n_clusters_final': len(np.unique(cluster_labels))
        })

        # 4. 클러스터별 크기 및 비율 로깅 (result.py에서 이동)
        for cluster_id, size in cluster_sizes.items():
            mlflow.log_metric(f"cluster_{cluster_id}_size", size)
            mlflow.log_metric(f"cluster_{cluster_id}_percent", size/len(df))
        
        # 5. 클러스터 중심점 로깅 (result.py에서 이동)
        for i, center in enumerate(cluster_centers):
            mlflow.log_param(f"cluster_{i}_center_x", center[0])
            mlflow.log_param(f"cluster_{i}_center_y", center[1])
            # 전체 중심점도 로깅 (다차원인 경우)
            mlflow.log_param(f"cluster_{i}_center", center.tolist())

        # 6. 모델 저장
        mlflow.sklearn.log_model(
            model, 
            "kmeans_model",
            registered_model_name="investment_clustering_model"
        )

        # 7. 클러스터 정보 파일 MLflow에 업로드 (result.py에서 이동)
        mlflow.log_artifact(str(cluster_info_path), "cluster_analysis")

        # 8. 시각화 및 아티팩트 저장
        plot_path = feature_pairs(df, n_clusters, cluster_labels, model, folder_path)

        # 시각화 파일이 생성되었다면 MLflow에 업로드
        if plot_path and os.path.exists(plot_path):
            mlflow.log_artifact(str(plot_path), "visualizations")
        
        # 추가로 다른 PNG 파일들도 업로드 (혹시 다른 시각화가 있다면)
        visualization_files = list(folder_path.glob("*.png"))
        
        for viz_file in visualization_files:
            if viz_file != plot_path:  # 이미 업로드한 파일은 제외
                mlflow.log_artifact(str(viz_file), "visualizations")
        
        # 9. 로컬 파일 정리 (MLflow 업로드 후)
        files_to_remove = [cluster_info_path]
        if plot_path:
            files_to_remove.append(plot_path)
        
        # 다른 시각화 파일들도 정리
        for viz_file in visualization_files:
            files_to_remove.append(viz_file)
        
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                os.remove(file_path)

        # 실행 정보 출력
        run_id = mlflow.active_run().info.run_id
        print(f"\n=== MLflow 실행 완료 ===")
        print(f"실행 ID: {run_id}")
        print(f"실험 이름: {experiment_name}")
        print(f"실행 이름: {run_name}")
        print(f"실루엣 점수: {silhouette_avg:.4f}")
        print(f"관성(Inertia): {inertia:.4f}")
        print(f"클러스터별 샘플 수: {cluster_sizes}")

        
    # DB 업데이트용 df
    update_df = clustered_df[["cluster_num"]].copy()
    update_df.loc[:,"invest_session_id"] = with_id_df["investSessionId"].values
    update_df.loc[:,"user_id"] = with_id_df["userId"].values

    return update_df

