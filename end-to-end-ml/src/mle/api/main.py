from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import mlflow.catboost
import numpy as np
import os

# 1. Инициализация
app = FastAPI(title="Purchase Prediction API", version="1.0")
MLFLOW_URI = "file:///home/jovyan/work/mlruns"  # Путь к артефактам
RUN_NAME = "purchase_v1_demo"

# 2. Загрузка модели (ленивая, при первом запросе)
_model = None
def load_model():
    global _model
    if _model is None:
        mlflow.set_tracking_uri(MLFLOW_URI)
        runs = mlflow.search_runs(filter_string=f"tags.mlflow.runName = '{RUN_NAME}'")
        if runs.empty:
            raise RuntimeError(f"❌ Run '{RUN_NAME}' not found in {MLFLOW_URI}")
        run_id = runs.iloc[0]["run_id"]
        model_uri = f"runs:/{run_id}/model"
        _model = mlflow.catboost.load_model(model_uri)
        print(f"✅ Модель загружена из run_id: {run_id}")
    return _model

# 3. Схема входных данных (валидация)
class UserFeatures(BaseModel):
    sessions_count: int = Field(..., ge=1, le=100)
    events_count: int = Field(..., ge=1, le=500)
    daily_spend: float = Field(..., ge=0.0, le=10000.0)
    unique_event_types: int = Field(..., ge=1, le=10)

# 4. Эндпоинт предсказания
@app.post("/predict")
async def predict(features: UserFeatures):
    model = load_model()
    df = pd.DataFrame([features.dict()])
    
    # Предсказание
    proba = model.predict_proba(df)[0, 1]
    label = int(proba > 0.5)
    
    # 🔹 Простая детекция дрейфа (сравнение с тренировочным распределением)
    # В продакшене: сравнивать с эталонными статистиками из MLflow
    drift_score = 0.0
    if features.daily_spend > 2000:  # Эвристика: аномально высокий чек
        drift_score = 0.8
    elif features.sessions_count > 50:  # Аномальная активность
        drift_score = 0.6
    
    return {
        "user_id": None,  # В реальном сервисе: извлекаем из JWT/headers
        "prediction": label,
        "probability": round(float(proba), 4),
        "drift_score": round(drift_score, 2),
        "model_version": RUN_NAME
    }

# 5. Health check
@app.get("/health")
async def health():
    return {"status": "ok", "service": "purchase-predictor"}
