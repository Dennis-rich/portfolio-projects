# ═══════════════════════════════════════════════════════════
# 🐳 Dockerfile для Amazon Reviews RAG Bot
# ═══════════════════════════════════════════════════════════

# Базовый образ Python 3.12
FROM python:3.12-slim

# Рабочая директория в контейнере
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём папки для данных (если не существуют)
RUN mkdir -p data/raw data/processed data/vector_db reports/evaluation

# Порт для Gradio (если нужно)
EXPOSE 7860

# Переменные окружения
ENV PROJECT_PATH=/app
ENV BOT_TOKEN=your_token_here

# Команда для запуска Telegram-бота
CMD ["python", "src/telegram_bot.py"]