import mlflow
import mlflow.sklearn
from invest.mlflow_config import get_mlflow_client  # 이 import 유지
import numpy as np
from pathlib import Path
import pandas as pd
import os

# airflow 용 import
from invest.models.kmeans import kmeans
from invest.models.result import result
from invest.models.feature_pairs import feature_pairs

def model_train(with_id_df):
    # MLflow 설정 - mlflow_config.py 사용
    mlflow_client = get_mlflow_client()
    
    # investSessionId drop : 모델링용 데이터
    df = with_id_df.drop(["userId", "investSessionId"], axis=1)

    # 현재 스크립트 파일의 디렉토리 가져오기
    current_script_dir = Path(__file__).parent.resolve()
    
    # 시각화.png, 모델 결과.pkl 저장경로 지정 (현재 스크립트 위치 기준)
    folder_path = current_script_dir / 'models'
    folder_path.mkdir(exist_ok=True)  # 폴더 생성

    # mlflow 실행 이름 설정
    run_name = f"kmeans_clustering_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
    
    # MLflow 실행을 함수 전체에서 관리
    with mlflow.start_run(run_name=run_name):
        try:
            print(f"🚀 MLflow 실행 시작: {run_name}")
            
            # 1. 데이터 정보 로깅
            data_params = {
                'data_shape': f"{df.shape[0]}x{df.shape[1]}",
                'feature_count': df.shape[1],
                'sample_count': df.shape[0],
                'feature_names': str(list(df.columns))
            }
            mlflow.log_params(data_params)

            # K-means 모델 파라미터 설정
            n_clusters = 5
            init_method = 'k-means++'
            max_iter = 300
            n_init = 10
            random_state = 42

            # 2. 하이퍼파라미터 로깅
            model_params = {
                'n_clusters': n_clusters,
                'init_method': init_method,
                'max_iter': max_iter,
                'n_init': n_init,
                'random_state': random_state,
                'algorithm': 'K-means'
            }
            mlflow.log_params(model_params)
            
            # 모델 학습 및 예측
            print("📊 모델 학습 시작...")
            model, cluster_labels, clustered_df = kmeans(df, n_clusters, init_method, max_iter, n_init, random_state)

            # 모델 평가 
            print("📈 모델 평가 중...")
            silhouette_avg, inertia, cluster_sizes, cluster_centers, cluster_info_path = result(df, model, cluster_labels, folder_path)
            
            # 3. 메트릭 로깅
            metrics = {
                'silhouette_score': float(silhouette_avg),
                'inertia': float(inertia),
                'n_clusters_final': int(len(np.unique(cluster_labels)))
            }
            mlflow.log_metrics(metrics)

            # 4. 클러스터별 크기 및 비율 로깅
            cluster_metrics = {}
            for cluster_id, size in cluster_sizes.items():
                cluster_metrics[f"cluster_{cluster_id}_size"] = int(size)
                cluster_metrics[f"cluster_{cluster_id}_percent"] = float(size/len(df))
            
            mlflow.log_metrics(cluster_metrics)
            
            # 5. 클러스터 중심점 로깅
            center_params = {}
            for i, center in enumerate(cluster_centers):
                if len(center) >= 2:
                    center_params[f"cluster_{i}_center_x"] = float(center[0])
                    center_params[f"cluster_{i}_center_y"] = float(center[1])
                center_params[f"cluster_{i}_center"] = str(center.tolist())
            
            mlflow.log_params(center_params)

            # 6. 모델 저장 (등록 없이 로깅만)
            print("💾 모델 저장 중...")
            try:
                # registered_model_name 제거하고 단순 로깅만 수행
                mlflow.sklearn.log_model(
                    model, 
                    "kmeans_model"
                    # registered_model_name 제거
                )
                print("✅ 모델 저장 완료")
            except Exception as model_error:
                print(f"⚠️ 모델 저장 실패: {model_error}")
                # 모델 저장 실패해도 계속 진행

            # 7. 클러스터 정보 파일 MLflow에 업로드
            if cluster_info_path and os.path.exists(cluster_info_path):
                try:
                    mlflow.log_artifact(str(cluster_info_path), "cluster_analysis")
                    print("✅ 클러스터 분석 파일 업로드 완료")
                except Exception as artifact_error:
                    print(f"⚠️ 클러스터 분석 파일 업로드 실패: {artifact_error}")

            # 8. 시각화 및 아티팩트 저장
            print("🎨 시각화 생성 중...")
            try:
                plot_path = feature_pairs(df, n_clusters, cluster_labels, model, folder_path)

                # 시각화 파일이 생성되었다면 MLflow에 업로드
                if plot_path and os.path.exists(plot_path):
                    mlflow.log_artifact(str(plot_path), "visualizations")
                    print("✅ 시각화 파일 업로드 완료")
                
                # 추가로 다른 PNG 파일들도 업로드
                visualization_files = list(folder_path.glob("*.png"))
                
                for viz_file in visualization_files:
                    if viz_file != plot_path:
                        try:
                            mlflow.log_artifact(str(viz_file), "visualizations")
                        except Exception as viz_error:
                            print(f"⚠️ 시각화 파일 업로드 실패: {viz_file}, {viz_error}")
            except Exception as viz_error:
                print(f"⚠️ 시각화 생성 실패: {viz_error}")
            
            # 9. 로컬 파일 정리
            files_to_remove = []
            if cluster_info_path:
                files_to_remove.append(cluster_info_path)
            if 'plot_path' in locals() and plot_path:
                files_to_remove.append(plot_path)
            
            # 다른 시각화 파일들도 정리
            if 'visualization_files' in locals():
                files_to_remove.extend(visualization_files)
            
            for file_path in files_to_remove:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as cleanup_error:
                    print(f"⚠️ 파일 삭제 실패: {file_path}, {cleanup_error}")

            # 성공 상태 명시적으로 설정
            mlflow.set_tag("status", "SUCCESS")
            mlflow.set_tag("execution_status", "COMPLETED")

            # 실행 정보 출력
            run_id = mlflow.active_run().info.run_id
            experiment_name = mlflow.get_experiment(mlflow.active_run().info.experiment_id).name
            
            print(f"\n=== MLflow 실행 완료 ===")
            print(f"🆔 실행 ID: {run_id}")
            print(f"🧪 실험 이름: {experiment_name}")
            print(f"🏃 실행 이름: {run_name}")
            print(f"📊 실루엣 점수: {silhouette_avg:.4f}")
            print(f"📈 관성(Inertia): {inertia:.4f}")
            print(f"👥 클러스터별 샘플 수: {cluster_sizes}")
            print(f"🌐 MLflow UI: http://43.203.175.69:5001")

        except Exception as e:
            print(f"❌ MLflow 실행 중 오류 발생: {e}")
            import traceback
            print(f"📋 상세 오류:\n{traceback.format_exc()}")
            
            # 실패 상태 설정
            mlflow.set_tag("status", "FAILED")
            mlflow.set_tag("error_message", str(e))
            
            # 예외를 다시 발생시키지 않고 계속 진행
            
    # DB 업데이트용 df (with 블록 밖에서 실행)
    try:
        update_df = clustered_df[["cluster_num"]].copy()
        update_df.loc[:,"invest_session_id"] = with_id_df["investSessionId"].values
        update_df.loc[:,"user_id"] = with_id_df["userId"].values
        return update_df
    except Exception as df_error:
        print(f"⚠️ 결과 DataFrame 생성 실패: {df_error}")
        # 빈 DataFrame 반환
        return pd.DataFrame({
            'cluster_num': [],
            'invest_session_id': [],
            'user_id': []
        })
