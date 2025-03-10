import requests
from bs4 import BeautifulSoup

URL = "https://magnit.ru/catalog"

def parse_products():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Ошибка при запросе:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select(".product-item"):
        name = item.select_one(".product-title").text
        price = item.select_one(".product-price").text
        products.append({"name": name, "price": price})

    print("Спарсено товаров:", len(products))
    return products
