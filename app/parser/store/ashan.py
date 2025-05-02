import time
from fake_useragent import UserAgent

from db.pw_model import Product
from requests import Session
from store.stocks_info import Stock

ua = UserAgent()
class AshanParser:
    store_id = 1
    store_code = 'ashan'

    def __init__(self, stock: Stock):
        self.stock = stock
        self.client = Session()
        self.client.headers.update(
            {'User-Agent': ua.random}
        )

    def fetch_categories(self):
        url = 'https://www.auchan.ru/v3/categories/'

        payload = {'active_only': 1, 'cashback_only': 0, 'promo_only': 0, 'show_hidden': 0, 'merchant_id': 43}

        r = self.client.get(url, params=payload)

        if r.status_code == 200:
            try:
                data = r.json()
                categories = []

                for _, ctg in enumerate(data):
                    category = {
                        'name': ctg['name'],
                        'code': ctg['code'],
                        'children': []
                    }
                    for _, subctg in enumerate(ctg['items']):
                        subcategory = {
                            'name': subctg['name'],
                            'code': subctg['code'],
                            'count': subctg['activeProductsCount']
                        }
                        category['children'].append(subcategory)
                    categories.append(category)
            except:
                print("Ошибка при разборе JSON:")
                print("Ответ сервера:", r.text[:500])
        else:
            print("Ошибка запроса:", r.text[:500])
        return categories

    def fetch_products(self, category, per_page=100, sleep_sec=1, v=False):
        page = 1
        num_parsed = 0
        total_count = 0

        product = []
        ids = set()

        while num_parsed == 0 or num_parsed < total_count:
            url = f'https://www.auchan.ru/v3/catalog/products/?merchantId={self.stock.stock_id}&perPage={per_page}&page={page}'

            payload = {
                "filter": {
                    "cashback_only": False,
                    "active_only": True,
                    "promo_only": False,
                    "category": category
                }
            }

            r = self.client.post(url, json=payload)
            data = r.json()

            total_count = data['activeRange']
            num_parsed += len(data['items'])
            if total_count - num_parsed < per_page:
                per_page = total_count - num_parsed

            page += 1

            if v:
                print('url', url, 'total', total_count)

            for item in data['items']:
                if item['id'] not in ids:
                    product.append(
                        {
                            'id': item['id'],
                            'name': item['title'],
                            'code': item['code'],
                            'price': item['price']['value']
                        }
                    )
                    ids.add(item['id'])
            time.sleep(sleep_sec)
        return product

    def start(self) -> list[Product]:
        ctgs = self.fetch_categories()

        all_products = []

        for ctg in ctgs:
            time.sleep(1)
            print(AshanParser.store_code, self.stock.region, ctg['code'])
            products = self.fetch_products(
                category=ctg['code'], v=False, sleep_sec=0.2)
            data = [
                Product(
                    product_id=f"{AshanParser.store_code}-{p['id']}",
                    store_id=AshanParser.store_id,
                    region_id=self.stock.region_id,
                    name=p['name'],
                    code=p['code'],
                    category=ctg['name'],
                    category_code=ctg['code'],
                    price=p['price']
                ) for p in products
            ]
            all_products += data

        return all_products
