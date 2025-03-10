from fastapi import APIRouter, BackgroundTasks
from app.services.parser_service import parse_products

router = APIRouter(prefix="/parser", tags=["Parser"])

@router.post("/start")
async def start_parsing(background_tasks: BackgroundTasks):
    background_tasks.add_task(parse_products)
    return {"message": "Парсинг запущен"}
