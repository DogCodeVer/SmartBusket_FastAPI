# FastAPI Project

## Описание
Этот проект представляет собой веб-приложение на FastAPI. Доступ к API ограничен только для IP-адреса `192.168.0.72`.

## Требования
- Python 3.9+
- Git
- Virtualenv

## Установка и запуск

1. **Клонирование репозитория:**
   ```sh
   git clone https://github.com/your-repo/your-project.git
   cd your-project
   ```

2. **Создание и активация виртуального окружения:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Для Linux/macOS
   .venv\Scripts\activate     # Для Windows
   ```

3. **Установка зависимостей:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Запуск сервера FastAPI:**
   ```sh
   uvicorn app.main:app --host 192.168.0.72 --port 8000
   ```

## Проверка работы
После запуска сервера API будет доступен по адресу:
```
http://192.168.0.72:8000
```

Документация Swagger доступна по адресу:
```
http://192.168.0.72:8000/docs
```

## Дополнительно
- Для выхода из виртуального окружения используйте команду:
  ```sh
  deactivate
  ```
- Убедитесь, что IP `192.168.0.72` назначен вашему устройству перед запуском сервера.

## Контакты
Если у вас возникли вопросы или проблемы, свяжитесь с разработчиком через [GitHub Issues](https://github.com/your-repo/your-project/issues).

