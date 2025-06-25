import os
import mlflow
from dotenv import load_dotenv

load_dotenv()

class MLflowConfig:
    def __init__(self):
        self.tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
        self.experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'invest_model_training')
    
    def setup_mlflow(self):
        """MLflow 클라이언트 설정 및 실험 생성"""
        mlflow.set_tracking_uri(self.tracking_uri)
        
        # 실험이 없으면 생성
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment is None:
                mlflow.create_experiment(self.experiment_name)
        except Exception as e:
            print(f"실험 설정 중 오류: {e}")
        
        mlflow.set_experiment(self.experiment_name)
        return mlflow

def get_mlflow_client():
    config = MLflowConfig()
    return config.setup_mlflow()
