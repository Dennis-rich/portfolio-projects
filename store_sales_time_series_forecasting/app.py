import streamlit as st
import json
import pandas as pd
from pathlib import Path
from catboost import CatBoostRegressor

@st.cache_resource
def load_model():
    model = CatBoostRegressor()
    model.load_model("models/catboost_A_final.cbm")
    return model

with open("models/model_features.json", "r") as f:
    meta = json.load(f)

feature_columns = meta["feature_columns"]

st.set_page_config(page_title="Store Sales Forecast", page_icon="🛒")
st.title("🛒 Прогноз продаж (Store Sales)")
st.markdown("Демо стриминговой модели. Использует реальные фичи из проекта.")

# Поля для ввода (можно расширить позже)
family = st.selectbox("Семейство товара", ["GROCERY I", "PRODUCE", "DAIRY", "BEVERAGES"], index=0)
city = st.selectbox("Город", ["Babahoyo", "Quito", "Guayaquil"], index=0)
store_type = st.selectbox("Тип магазина", ["B", "A", "C"], index=0)
onpromotion = st.slider("Товаров по акции", 0, 100, 66)
sales_lag_7 = st.number_input("Продажи 7 дней назад", value=5869.87)

# Остальные фичи — фиксированные (на основе твоего примера)
input_data = {
    "family": family,
    "city": city,
    "state": "Los Rios",          # можно сделать selectbox позже
    "store_type": store_type,
    "onpromotion": onpromotion,
    "promo_effect": 0,            # упрощено
    "month": 8,
    "day_of_week": 5,
    "is_weekend": 1,
    "is_month_start": 0,
    "is_month_end": 0,
    "is_national_holiday": 0,
    "is_regional_holiday": 0,
    "cluster": 10,
    "sales_lag_7": sales_lag_7,
    "sales_lag_14": sales_lag_7 * 0.8,  # приблизительно
    "sales_lag_21": sales_lag_7 * 0.85,
    "onpromotion_lag_7": float(onpromotion),
    "onpromotion_lag_14": float(onpromotion) * 0.9,
}

missing = set(feature_columns) - set(input_data.keys())
if missing:
    st.error(f"Ошибка: не хватает фичей {missing}")
else:
    df = pd.DataFrame([input_data])[feature_columns]
    model = load_model()
    if st.button("Предсказать"):
        pred = model.predict(df)[0]
        st.success(f"**Прогноз продаж**: {pred:.2f}")
