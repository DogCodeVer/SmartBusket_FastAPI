import re
import requests
from bs4 import BeautifulSoup

pattern = r"(\d+([.,]\d+)?)\s?(г|кг|л|мл|gr|kg|ml)\b"

def parse_products(shop_code='963529', max_pages=50):
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
