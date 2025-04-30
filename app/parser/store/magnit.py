import time
from uuid import uuid4

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import Session

from db.pw_model import Product
from store.stocks_info import Stock

INCLUDE_IDS = {'58685', '61481', '60269', '47161', '4435', '48463', '48465', '40293'}


def get_subcategory_ids(category_codes: list[str]) -> list[int]:
    return [int(code.split('-', 1)[0]) for code in category_codes]

ua = UserAgent()
class MagnitParser:
    store_id = 2
    store_code = 'magnit'

    def __init__(self, stock: Stock) -> None:
        self.stock = stock
        client = Session()
        client.headers.update({
            'User-Agent': ua.random,
            'X-Device-Id': str(uuid4()).upper(),
            'X-App-Version': '7.0.0',
            'X-Client-Name': 'magnit',
            'X-Client-Platform': 'Web',
            'X-Device-Tag': 'disabled',
            'X-Platform-Version': 'Windows Chrome 135',
            'Origin': 'https://magnit.ru',
        })
        self.client = client

    def total_products(self) -> int:
        url = 'https://magnit.ru/webgate/v2/goods/search'
        payload = {
            "sort": {"order": "desc", "type": "popularity"},
            "pagination": {"limit": 33, "offset": 0},
            "includeAdultGoods": True,
            "storeCode": self.stock.stock_id,
            "storeType": "1",
            "catalogType": "1"
        }
        response = self.client.post(url, json=payload)
        return response.json()['pagination']['totalCount']

    def fetch_categories(self) -> list[str]:
        url = 'https://magnit.ru/'
        response = self.client.get(url, cookies={'shopCode': self.stock.stock_id})
        soup = BeautifulSoup(response.text, "html.parser")

        categories = []
        for item in soup.find_all('div', class_='pl-list-item__title'):
            a_tag = item.find('a')
            if a_tag and '/catalog/' in a_tag['href']:
                cat_code = a_tag['href'].replace('/catalog/', '')
                if cat_code.split('-')[0] not in INCLUDE_IDS:
                    categories.append(cat_code)
        return categories

    def fetch_subctg(self, ctg_id: list) -> list:
        url = 'https://magnit.ru/catalog/'
        all_sub_ctg = []

        for i in ctg_id:
            r = self.client.get(url + i, cookies={'shopCode': self.stock.stock_id})
            data = BeautifulSoup(r.text, 'html.parser')

            for j in data.find_all('div', class_='filters-category__children'):
                a_tags = j.find_all('a')
                for a in a_tags:
                    href = a.get('href')
                    if href and '/catalog/' in href:
                        clean_href = href.split('?')[0].replace('/catalog/', '')
                        all_sub_ctg.append(clean_href)
            time.sleep(0.2)

        return all_sub_ctg

    def fetch_products(self, category_id: int, verbose=False, sleep_sec=1) -> list[dict]:
        url = 'https://magnit.ru/webgate/v2/goods/search'
        products = []
        offset = 0
        limit = 33
        total = 1

        while offset < total:
            payload = {
                "sort": {"order": "desc", "type": "popularity"},
                "pagination": {"limit": limit, "offset": offset},
                "categories": [category_id],
                "includeAdultGoods": True,
                "storeCode": self.stock.stock_id,
                "storeType": "6",
                "catalogType": "1"
            }

            response = self.client.post(url, json=payload)
            data = response.json()

            if not data['items']:
                if verbose:
                    print(f'Category {category_id} has no products.')
                break

            total = data['pagination']['totalCount']
            offset += limit

            for item in data['items']:
                products.append({
                    'id': item['id'],
                    'name': item['name'],
                    'code': item['productId'],
                    'price': item['price'] // 100
                })

            if verbose:
                print(f'Fetched {len(products)} products from category {category_id}')
            time.sleep(sleep_sec)

        return products

    def start(self) -> list[Product]:
        ctgs = self.fetch_categories()
        ctg_ids = self.fetch_subctg(ctgs)
        all_products = []

        for ctg in ctg_ids:
            time.sleep(1)
            print(MagnitParser.store_code, self.stock.region, ctg)

            products = self.fetch_products(ctg)

            data = [Product(product_id=f'{MagnitParser.store_code}-{p["id"]}',
                            store_id=MagnitParser.store_id,
                            region_id=self.stock.region_id,
                            name=p['name'],
                            code=p['code'],
                            category=ctg['name'],
                            category_code=ctg['code'],
                            price=p['price']) for p in products]
            all_products += data

        return all_products
