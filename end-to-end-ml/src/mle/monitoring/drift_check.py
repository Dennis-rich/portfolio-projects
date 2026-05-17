import pandas as pd
import numpy as np
from scipy import stats

def check_drift(reference_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.1):
    """Простой KS-тест для каждой фичи"""
    drift_report = {}
    for col in reference_df.columns:
        if col in current_df.columns and np.issubdtype(reference_df[col].dtype, np.number):
            ks_stat, p_value = stats.ks_2samp(reference_df[col].dropna(), current_df[col].dropna())
            drift_report[col] = {"ks_stat": round(ks_stat, 3), "drifted": ks_stat > threshold}
    return drift_report

# Пример использования (в Airflow DAG или cron)
# ref = pd.read_parquet("s3://features/train_sample.parquet")
# curr = pd.read_parquet("s3://features/daily_batch.parquet")
# report = check_drift(ref, curr)
# if any(v["drifted"] for v in report.values()):
#     trigger_retraining()
