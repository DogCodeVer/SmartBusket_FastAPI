# Используем Python 3.11 в качестве базового образа
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем необходимые файлы для работы alembic
COPY requirements.txt ./
COPY alembic.ini ./
COPY wait-for-it.sh /app/wait-for-it.sh

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в контейнер
COPY ./app ./app

# Делаем wait-for-it.sh исполнимым
RUN chmod +x /app/wait-for-it.sh

# Указываем команду для запуска миграций Alembic
CMD ["alembic", "upgrade", "head"]
