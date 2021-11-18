import requests
import json
import config

class APIException(Exception):
    pass

class cryptoAPI:
    @staticmethod
    def get_price(base,quote,amount):
        res = {'value':0.0,'error':0}
        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={config.APIkey}')  # делаем запрос на сервер по переданному адресу
        except Exception:
            res['error'] = -2
            return res

        texts = json.loads(r.content)  # из формата json конверируем в словарь
        try:
            val = amount * texts[quote]
        except ValueError:
            res['error'] = -1
            return res
        res['value'] = val
        return res


