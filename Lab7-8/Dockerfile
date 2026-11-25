# Образ із Python на основі Alpine Linux.
FROM python:3.12-alpine 

# Робоча папка.
WORKDIR /app

# Виводимо логи Python без буферизації.
ENV PYTHONUNBUFFERED=1 

# Спочатку встановлюємо залежності.
COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код вебзастосунку.
COPY app.py ./ 

# Документуємо порт, який використовує програма.
EXPOSE 8080 

# Запускаємо вебзастосунок.
CMD ["python", "app.py"] 