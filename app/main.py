from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import parser

app = FastAPI(title="Food Product Parser")

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любого домена (на этапе разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешает все заголовки
)

# Подключаем роутеры
app.include_router(parser.router)
