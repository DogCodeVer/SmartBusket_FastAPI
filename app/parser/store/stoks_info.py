import json

class Stock:
    def __init__(self, region: str, stock_id: int, region_id: int) -> None:
        self.region = region
        self.region_id = region_id
        self.stock_id = stock_id


def _read_stocks(dir, code, prefix) -> list[Stock]:
    with open(f"{dir}/{prefix}_{code}.json", 'r', encoding='utf-8') as file:
        return [Stock(**stock) for stock in json.load(file)['stocks']]


class StocksInfo:
    def __init__(self, store_code = "", stock_list_prefix = "stocks", dir='data') -> None:
        self.stocks = _read_stocks(dir,store_code, stock_list_prefix)

