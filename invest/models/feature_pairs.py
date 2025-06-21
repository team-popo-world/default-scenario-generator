import matplotlib.pyplot as plt
import itertools
import mlflow
import os

def feature_pairs(df, n_clusters, cluster_labels, model, folder_path):
    # 시각화(컬럼 별 군집화 결과)
    X_scaled = df.values
    feature_names = df.columns.tolist()

    # 클러스터별 색상 정의
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
    cluster_colors = colors[:n_clusters]


    # 3. 간단한 버전 - 모든 조합을 한 번에 보기
    n_features = len(feature_names)
    feature_combinations = list(itertools.combinations(range(n_features), 2))
    n_combinations = len(feature_combinations)

    if n_combinations > 0:
        # 적절한 그리드 크기 계산
        cols = min(4, n_combinations)
        rows = (n_combinations + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        fig.suptitle('All Feature Pair Combinations', fontsize=16, y=1.02)
        
        # axes를 1D로 변환
        if n_combinations == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if rows > 1 or cols > 1 else [axes]
        
        for idx, (i, j) in enumerate(feature_combinations):
            ax = axes[idx]
            
            # 클러스터별 점들
            for cluster_id in range(n_clusters):
                cluster_mask = cluster_labels == cluster_id
                cluster_points = X_scaled[cluster_mask]
                
                if len(cluster_points) > 0:
                    ax.scatter(cluster_points[:, j], cluster_points[:, i], 
                            c=cluster_colors[cluster_id], alpha=0.7, s=40,
                            label=f'Cluster {cluster_id}')
            
            # 중심점
            for cluster_id in range(n_clusters):
                center = model.cluster_centers_[cluster_id]
                ax.scatter(center[j], center[i], 
                        c=cluster_colors[cluster_id], marker='x', 
                        s=200, linewidths=3)
            
            ax.set_xlabel(f'{feature_names[j]}')
            ax.set_ylabel(f'{feature_names[i]}')
            ax.set_title(f'{feature_names[i]} vs {feature_names[j]}')
            ax.grid(True, alpha=0.3)
            
            if idx == 0:
                ax.legend(fontsize=8)
        
        # 빈 서브플롯 숨기기
        for idx in range(n_combinations, len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])

        # 시각화 저장
        plot_path = folder_path / "all_feature_pairs.png"
        plt.savefig(str(plot_path), dpi=300, bbox_inches='tight')
        mlflow.log_artifact(str(plot_path))
        plt.show()


    # 파일 정리 (MLflow 업로드 후 로컬 파일 삭제)
    if os.path.exists(plot_path):
        os.remove(plot_path)
    