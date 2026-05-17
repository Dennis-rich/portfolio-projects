# 🚀 End-to-End ML Pipeline: Purchase Prediction

Проект демонстрирует полный цикл работы с данными: от сырого потока событий до деплоя модели в продакшен-подобной среде.

## 🎯 Бизнес-задача
Предсказать, совершит ли пользователь покупку в ближайшие 7 дней, на основе его поведения в приложении.

## 🏗️ Архитектура
[Backend Sim] → Kafka → [Spark DE] → Parquet → [CatBoost DS] → MLflow → [FastAPI MLE] → API

### Компоненты:
| Роль | Инструменты | Задача |
|------|-------------|--------|
| **Backend Sim** | Python, `kafka-python` | Генерация событий (клик, просмотр, покупка) |
| **Data Engineer** | PySpark, Kafka, Parquet | Очистка, оконные функции, агрегация до витрины `user × day` |
| **Data Scientist** | CatBoost, MLflow, scikit-learn | Обучение модели, оценка, логирование артефактов, детекция дрифта (KS-тест) |
| **ML Engineer** | FastAPI, Docker, uvicorn | Деплой модели, health-check, валидация входа (Pydantic) |

## 🛠 Стек
- **Data:** Kafka, PySpark, Parquet, Pandas, SQL
- **ML:** CatBoost, Scikit-learn, SHAP, KS-test
- **MLOps:** MLflow, FastAPI, Docker, Docker Compose
- **Infra:** Python 3.10, Jupyter

## 🚀 Быстрый старт

```bash
# 1. Запустить инфраструктуру (Kafka, Spark, API)
docker compose up -d

# 2. Сгенерировать тестовые данные
cd src/backend_sim
python3 producer.py  # Нажми Ctrl+C после 10-15 сек

# 3. Запустить DE-пайплайн
# Открой Jupyter: http://localhost:8888
# Запусти: src/de/01_extract_clean.ipynb → Run All

# 4. Обучить модель
# Запусти: src/ds/01_purchase_model.ipynb → Run All

# 5. Запустить API
docker compose up -d api

# 6. Проверить предсказание
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sessions_count": 3, "events_count": 12, "daily_spend": 650.5, "unique_event_types": 4}'

  ## 📊 Результаты (демо-данные)
| Метрика | Значение | Примечание |
|---------|----------|------------|
| ROC-AUC | 1.000* | Синтетический таргет (`daily_spend > 500`) |
| Precision@0.5 | 1.000* | На реальных данных ожидается 0.7–0.85 |

> *Идеальные метрики обусловлены синтетическим таргетом. В реальных данных ожидается 0.7–0.85.


## 🗂️ Структура проекта
end-to-end-ml/
├── 🐳 docker-compose.yml      # Инфраструктура (Kafka, Spark, API)
├── 📁 data/                   # Витрины Parquet (не коммитить)
├── 📁 src/
│   ├── backend_sim/           # Генератор событий
│   ├── de/                    # PySpark: очистка и агрегация
│   ├── ds/                    # Обучение и валидация моделей
│   └── mle/                   # FastAPI API + мониторинг дрифта
├── 📁 schema/                 # Data contracts (JSON)
├── 📁 mlruns/                 # Логи MLflow (не коммитить)
└── 📄 README.md               # Описание проекта

## ⚠️ Важные заметки
- **Данные**: Папки `data/` и `mlruns/` добавлены в `.gitignore` — не коммить тяжёлые файлы.
- **Воспроизводимость**: Фиксированные `random_state`, версионирование через MLflow.
- **Масштабирование**: Партиционирование Parquet по дате, идемпотентная загрузка.

## 👤 Автор
**Денис Решетов**
📍 Саратов, Россия
📧 denis.reshetov.ds@outlook.com
🔗 [GitHub](https://github.com/Dennis-rich/portfolio-projects) | [Telegram](https://t.me/den_rich_r)
