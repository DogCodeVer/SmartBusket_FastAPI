from fastapi import APIRouter, HTTPException
from app.services.parser_service import *
import logging

router = APIRouter(prefix="/parser", tags=["Parser"])

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/start")
async def start_parsing():
    try:
        logger.info("Запуск парсинга...")
        products = parse_products()  # Синхронный вызов
        if not products:
            raise HTTPException(status_code=404, detail="Товары не найдены")
        return {"message": "Парсинг завершён", "products": products}
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка парсинга: {str(e)}")

@router.get("/get_category")
async def get_category():
    try:
        logger.info("Получение категорий")
        categories = parse_category()
        if not categories:
            raise HTTPException(status_code=404, detail="Нет категорий")
        return categories
    except Exception as e:
        logger.error(f"Ошибка при получение категорий: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка парсинга: {str(e)}")

@router.get("/get_products/{category_id}")
async def fetch_products(category_id: str):
    try:
        logger.info("Получение товаров")
        products = parse_products_list(category_id)
        if not products:
            raise HTTPException(status_code=404, detail="Products not found")
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/get_product_info/{product_id}")
async def fetch_product_info(product_id: str):
    try:
        logger.info("Получение информации о товаре")
        product_info = parse_product_info(product_id)
        if not product_info:
            raise HTTPException(status_code=404, detail="Product not found")
        return product_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

