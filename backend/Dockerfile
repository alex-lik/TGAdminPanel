FROM python:3.13-slim

WORKDIR /app
<<<<<<< HEAD
=======
# Установка зависимостей системы для Celery и Flower
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
>>>>>>> abd87a6c29e9f56783cac546c133769c128e472a

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

<<<<<<< HEAD
COPY app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
=======
# COPY app /app/app
# COPY app /app/app
COPY app/ /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8015"]
>>>>>>> abd87a6c29e9f56783cac546c133769c128e472a
