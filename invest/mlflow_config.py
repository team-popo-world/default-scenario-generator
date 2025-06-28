import os
import mlflow
from dotenv import load_dotenv

load_dotenv()

class MLflowConfig:
    def __init__(self):
        # 환경변수에서 가져오되, 없으면 기본값 사용
        self.tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://43.203.175.69:5001')
        self.experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'invest_model_training')
    
    def setup_mlflow(self):
        """MLflow 클라이언트 설정 및 실험 생성"""
        print(f"🔗 MLflow tracking URI 설정: {self.tracking_uri}")
        mlflow.set_tracking_uri(self.tracking_uri)
        
        # 실험 설정
        try:
            # 기존 실험 확인
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment is None:
                # 실험이 없으면 생성
                experiment_id = mlflow.create_experiment(self.experiment_name)
                print(f"✅ 새 실험 생성: {self.experiment_name} (ID: {experiment_id})")
            else:
                print(f"✅ 기존 실험 사용: {self.experiment_name} (ID: {experiment.experiment_id})")
            
            # 실험 설정
            mlflow.set_experiment(self.experiment_name)
            
        except Exception as e:
            print(f"❌ 실험 설정 중 오류: {e}")
            # 오류 발생 시 기본 실험 사용
            mlflow.set_experiment("Default")
        
        return mlflow

def get_mlflow_client():
    """MLflow 클라이언트 반환"""
    config = MLflowConfig()
    return config.setup_mlflow()
