import json, time, uuid, random
from datetime import datetime, timezone
from faker import Faker
from kafka import KafkaProducer

fake = Faker()
KAFKA_BOOTSTRAP = 'localhost:9092'
TOPIC = 'raw_events'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_event():
    user_id = random.randint(1000, 1999)
    is_test = user_id == 1999  # 0.1% тестовых пользователей
    
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "event_type": random.choice(["view", "click", "add_to_cart", "purchase", "login", "logout"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "product_id": random.randint(100, 999) if random.random() > 0.2 else None,
        "amount": round(random.uniform(10, 500), 2) if random.random() > 0.3 else None,
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "session_id": str(uuid.uuid4()),
        "is_test": is_test
    }
    
    # 🔹 ВНЕДРЯЕМ ГРЯЗЬ (5-7% событий)
    dirt = random.random()
    if dirt < 0.02: event["amount"] = -50.0          # Отрицательная сумма
    elif dirt < 0.04: event["user_id"] = None          # NULL в ключе
    elif dirt < 0.05: event["timestamp"] = "yesterday" # Кривой timestamp
    elif dirt < 0.06: del event["event_type"]          # Пропущенное обязательное поле
        
    return event

print(f"🚀 Запуск продюсера. Топик: {TOPIC}, Сервер: {KAFKA_BOOTSTRAP}")
count = 0
try:
    while True:
        event = generate_event()
        producer.send(TOPIC, value=event)
        count += 1
        if count % 10 == 0:
            print(f"✅ Отправлено {count} событий")
        time.sleep(0.5)  # 2 события/сек (легко для ноутбука)
except KeyboardInterrupt:
    print(f"\n🛑 Остановлено. Всего отправлено: {count}")
    producer.close()
