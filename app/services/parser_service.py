import re

import requests
from bs4 import BeautifulSoup

pattern = r"(\d+([.,]\d+)?)\s?(г|кг|л|мл|gr|kg|ml)\b"


def parse_products_magnit(shop_code='963529', max_pages=50):
    base_url = "https://magnit.ru/catalog"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    cookies = {'shopCode': shop_code}

    products = []
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers, cookies=cookies)

        if response.status_code != 200:
            print(f"Ошибка {response.status_code} на странице {page}")
            break

        soup = BeautifulSoup(response.content.decode("utf-8"), "lxml")
        cards = soup.find_all('article', class_='unit-catalog-product-preview show-ratings')

        if not cards:
            print(f"Страница {page} пустая, завершаем парсинг.")
            break

        print(f"Обрабатываем страницу {page}, товаров найдено: {len(cards)}")

        for card in cards:
            try:
                title = card.find('div', class_='pl-text unit-catalog-product-preview-title').text.strip()
                price_tag = card.find('span', class_='unit-catalog-product-preview-prices__regular')
                price = price_tag.text.strip() if price_tag else None

                value_tag = card.find('span', class_='pl-text unit-catalog-product-preview-unit-value')
                value = value_tag.text.strip() if value_tag else None

                # Ищем граммовку в названии
                match = re.search(pattern, title, flags=re.IGNORECASE)
                extracted_value = f"{match.group(1)} {match.group(3)}" if match else None

                # Если value пустой, берем из названия
                final_value = value if value else extracted_value

                # Убираем граммовку из названия
                clean_title = re.sub(pattern, "", title, flags=re.IGNORECASE).strip()

                products.append({
                    "title": clean_title,
                    "price": price,
                    "value": final_value,
                })
            except Exception as e:
                print(f"Ошибка парсинга карточки: {e}")

        page += 1
        if page > max_pages:  # Чтобы не зациклиться
            print("Достигнуто максимальное количество страниц.")
            break

    return products


def parse_category():
    global filtered_categories
    url = "https://5d.5ka.ru/api/catalog/v2/stores/Y232/categories"
    params = {
        "mode": "delivery",
        "include_subcategories": "1",
        "include_restrict": "true"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://5ka.ru",
        "X-App-Version": "tc5-v250312-31214353",
        "X-Device-Id": "f7261964-c7fa-4b75-94ee-693aa9a896e2",
        "X-Platform": "webapp",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        # Фильтруем категории, исключая "Пятёрочка выручает!" и "Готовая еда"
        excluded_categories = ["Пятёрочка выручает!", "Готовая еда"]
        filtered_categories = []

        for category in data:
            if category["name"] in excluded_categories:
                continue

            # Фильтруем субкатегории, исключая те, у которых advert не пустой
            filtered_subcategories = [
                subcat for subcat in category.get("categories", [])
                if not subcat.get("advert")
            ]

            # Если после фильтрации остались субкатегории, добавляем категорию
            if filtered_subcategories:
                category["categories"] = filtered_subcategories
                filtered_categories.append(category)

    return filtered_categories


def parse_products_list(category_id: str):
    url = f"https://5d.5ka.ru/api/catalog/v2/stores/Y232/categories/{category_id}/products"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://5ka.ru",
        "X-App-Version": "tc5-v250312-31214353",
        "X-Device-Id": "50123270-28fc-412d-9f50-66dc2316be61",
        "X-Platform": "webapp",
    }

    all_products = []  # Список для хранения всех товаров
    offset = 0  # Начинаем с 0
    limit = 20  # Можно увеличить, например, 50

    while True:
        # Формируем URL с параметрами
        params = {
            "mode": "delivery",
            "include_restrict": "true",
            "limit": limit,
            "offset": offset,
        }

        # Делаем запрос
        response = requests.get(url, headers=headers, params=params)

        # Проверяем, что запрос прошел успешно
        if response.status_code == 200:
            data = response.json()

            # Добавляем товары в список
            all_products.extend(data.get("products", []))

            # Если товаров меньше, чем лимит, значит это последняя страница
            if len(data.get("products", [])) < limit:
                break

            # Увеличиваем offset для следующей страницы
            offset += limit
        else:
            print(f"Ошибка запроса: {response.status_code}")
            break

    return all_products


def parse_product_info(product_id: str):
    url = f"https://5d.5ka.ru/api/catalog/v2/stores/Y232/products/{product_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://5ka.ru",
        "X-App-Version": "tc5-v250312-31214353",
        "X-Device-Id": "50123270-28fc-412d-9f50-66dc2316be61",
        "X-Platform": "webapp",
    }
    params = {
        "mode": "delivery",
        "include_restrict": "true",
    }

    product_info = ''
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        product_info = response.json()
    else:
        print(f"Ошибка запроса: {response.status_code}")

    return product_info


def parse_product_subcategories(category_id: str):
    url = f'https://5d.5ka.ru/api/catalog/v2/stores/Y232/categories/{category_id}/extended'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://5ka.ru",
        "X-App-Version": "tc5-v250312-31214353",
        "X-Device-Id": "50123270-28fc-412d-9f50-66dc2316be61",
        "X-Platform": "webapp",
    }
    params = {
        "mode": "delivery",
        "include_restrict": "true",
    }

    subcategories = []

    response = requests.get(url, headers=headers, params=params)

    print(response.json())

    if response.status_code == 200:
        data = response.json()
        subcategories = data


    else:
        print(f"Ошибка запроса: {response.status_code}")

    return subcategories
