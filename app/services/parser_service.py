import requests
from bs4 import BeautifulSoup

def parse_products(shop_code='963529'):
    url = "https://magnit.ru/catalog"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    cookies = {'shopCode': shop_code}

    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.content.decode("utf-8"), "lxml")

    # Найти карточки товаров
    cards = soup.find_all('article', class_='unit-catalog-product-preview show-ratings')

    # Список для хранения результатов
    products = []

    for card in cards:
        try:
            title = card.find('span', class_='product-title').text.strip()
            price = card.find('span', class_='price').text.strip()
            image_url = card.find('img', class_='product-image')['src']
            link = "https://magnit.ru" + card.find('a', class_='product-link')['href']

            products.append({
                "title": title,
                "price": price,
                "image_url": image_url,
                "link": link
            })
        except Exception as e:
            print(f"Ошибка парсинга карточки: {e}")

    return products
