# Используем Python 3.11 в качестве базового образа
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в контейнер
COPY ./app/fast_api ./app/fast_api

# Устанавливаем рабочую директорию для FastAPI
WORKDIR /app

# Указываем команду для запуска FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
