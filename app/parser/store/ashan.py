import time
from requests import Session

from db.pw_model import Product
from store.stocks_info import Stock

class AshanParser:

    store_id = 1
    store_code = 'ashan'

    def __init__(self, stock: Stock) -> None:
        self.stock = stock
        self.client = Session()
        self.client.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Linux; U; Linux i674 ) Gecko/20130401 Firefox/62.8'}
        )

    def fetch_categories(self):
        r = self.client.get(
            f'https://www.auchan.ru/v1/categories?max_depth=1&merchant_id={self.stock.stock_id}'
        )

        categories = []

        for _, ctg in enumerate(r.json()):
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

        return categories

    def fetch_products(self, category, per_page=100, sleep_sec=1, v=False):
        page = 1
        num_parsed = 0
        total_count = 0

        products = []
        ids = set()

        while num_parsed == 0 or num_parsed < total_count:
            url = (
                f'https://www.auchan.ru/v1/catalog/products?merchantId={self.stock.stock_id}'
                f'&page={page}&perPage={per_page}'
            )
            r = self.client.post(
                url, json={"filter": {"category": category, }, },)
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
                    products.append(
                        {'id': item['id'], 'name': item['title'], 'code': item['code'], 'price': item['price']['value']}
                    )
                    ids.add(item['id'])

            time.sleep(sleep_sec)

        return products

    def start(self) -> list[Product]:
        ctgs = self.fetch_categories()

        all_products = []

        for ctg in ctgs:
            time.sleep(1)
            print(AshanParser.store_code, self.stock.region, ctg['name'])
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
