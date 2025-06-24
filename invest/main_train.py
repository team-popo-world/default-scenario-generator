import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

from pathlib import Path

from main_preprocess import model_preprocess
from models.kmeans import kmeans
from models.result import result
from models.feature_pairs import feature_pairs


def model_train(with_id_df):
    # 모델 성능 추적: mlflow
    mlflow.set_tracking_uri("http://127.0.0.1:5000")

    # 실험 생성 또는 설정
    experiment_name = "clustering_experiment"
    try:
        experiment_id = mlflow.create_experiment(experiment_name)
    except mlflow.exceptions.MlflowException:
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

    mlflow.set_experiment(experiment_name)


    # investSessionId drop : 모델링용 데이터
    df = with_id_df.drop("investSessionId", axis=1)

    # 현재 스크립트 파일의 디렉토리 가져오기
    current_script_dir = Path(__file__).parent.resolve()
    
    # 시각화.png, 모델 결과.pkl 저장경로 지정 (현재 스크립트 위치 기준)
    folder_path = current_script_dir / 'models'


    with mlflow.start_run():

        # K-means 모델 파라미터 설정
        n_clusters = 5
        init_method = 'k-means++'
        max_iter = 300
        n_init = 10
        random_state = 42
        
        # 모델 학습 및 예측
        model, cluster_labels, clustered_df = kmeans(df, n_clusters, init_method, max_iter, n_init, random_state)
        print("clustered_df", clustered_df.head())

        # 모델 평가
        silhouette_avg, inertia, cluster_sizes = result(df, model, cluster_labels, folder_path)
        
        # 실행 정보 출력
        run_id = mlflow.active_run().info.run_id
        print(f"\n=== MLflow 실행 완료 ===")
        print(f"실행 ID: {run_id}")
        print(f"실험 이름: {experiment_name}")
        print(f"실루엣 점수: {silhouette_avg:.4f}")
        print(f"관성(Inertia): {inertia:.4f}")
        print(f"클러스터별 샘플 수: {cluster_sizes}")

        # 피쳐 별 군집 시각화
        feature_pairs(df, n_clusters, cluster_labels, model, folder_path)
        
    # DB 업데이트용 df
    update_df = clustered_df[["cluster_num"]].copy()
    update_df.loc[:,"invest_session_id"] = with_id_df["investSessionId"].values

    return update_df

