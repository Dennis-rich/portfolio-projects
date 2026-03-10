#!/usr/bin/env python3
"""
Прогноз продаж: CLI-инференс (с реальным примером из test_final).
"""

import json
import pandas as pd
from pathlib import Path
from catboost import CatBoostRegressor

MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "catboost_A_final.cbm"
META_PATH = MODEL_DIR / "model_features.json"

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

feature_columns = meta["feature_columns"]

# Пример реального запроса (из test_final)
input_data = {'family': 'GROCERY I', 'city': 'Babahoyo', 'state': 'Los Rios', 'store_type': 'B', 'onpromotion': 66, 'promo_effect': 0, 'month': 8, 'day_of_week': 5, 'is_weekend': 1, 'is_month_start': 0, 'is_month_end': 0, 'is_national_holiday': 0, 'is_regional_holiday': 0, 'cluster': 10, 'sales_lag_7': 5869.87, 'sales_lag_14': 4711.38, 'sales_lag_21': 4972.5, 'onpromotion_lag_7': 73.0, 'onpromotion_lag_14': 61.0}

missing = set(feature_columns) - set(input_data.keys())
if missing:
    raise ValueError(f"Не хватает фичей: {missing}")

df = pd.DataFrame([input_data])[feature_columns]

model = CatBoostRegressor()
model.load_model(str(MODEL_PATH))
prediction = model.predict(df)[0]

print(f"\n🎯 Прогноз продаж: {prediction:.2f}\n")
