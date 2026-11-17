# Базовий образ Alpine Linux.
FROM alpine:latest 

# Встановлюємо Python.
RUN apk add --no-cache python3 

# Робоча папка всередині контейнера.
WORKDIR /app 

# Налаштовуємо виведення Python та шлях до даних.
ENV PYTHONUNBUFFERED=1 
ENV PYTHONIOENCODING=utf-8
ENV ORDERS_FILE=/data/orders.json

# Копіюємо потрібні файли програми.
COPY order_manager.py main.py ./ 


# Створюємо папку для збереження даних.
RUN mkdir -p /data 


CMD ["python3", "main.py"] # Під час запуску контейнера запускаємо програму з меню.