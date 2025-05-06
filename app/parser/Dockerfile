# Используем Python 3.11 в качестве базового образа
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в контейнер
COPY ./app/parser ./app/parser

# Устанавливаем рабочую директорию для Parser
WORKDIR /app

# Указываем команду для запуска парсера
CMD ["python", "main.py"]
