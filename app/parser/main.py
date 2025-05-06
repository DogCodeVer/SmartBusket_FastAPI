from multiprocessing.pool import ThreadPool

from config import Config
from app.db.database import Db, create_engine_from_config
from store.ashan import AshanParser
from store.magnit import MagnitParser
from store.stoks_info import StocksInfo

BATCH_SIZE = 100


def remove_duplicates(products: list) -> list:
    seen = {}
    for obj in products:
        if obj.product_id not in seen:
            seen[obj.product_id] = obj
    return list(seen.values())


def parse_stores(parsers: list, db: Db):
    for parser in parsers:
        products = remove_duplicates(parser.start())
        db.add_products(products, BATCH_SIZE)
        print(f'{parser.__class__}_{parser.stock.region}: parsed products {len(products)}')


def parse():
    cfg = Config()
    cfg.read_from_env()

    driver = create_engine_from_config(cfg.dbconfig)
    db = Db(driver)
    db.connect()

    ashan_stocks = StocksInfo(AshanParser.store_code)
    magnit_stocks = StocksInfo(MagnitParser.store_code)

    mps = [MagnitParser(stock=s) for s in magnit_stocks.stocks]
    aps = [AshanParser(stock=s) for s in ashan_stocks.stocks]

    parse_group = [aps, mps]

    with ThreadPool(processes=len(parse_group)) as pool:
        for group in parse_group:
            pool.apply_async(func=parse_stores, args=(group, db))
        pool.close()
        pool.join()


if __name__ == '__main__':
    parse()
