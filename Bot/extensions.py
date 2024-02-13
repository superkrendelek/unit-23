import requests
import json
from config import keys

class ConvertionExeption(Exception):
    pass

class APIException:
    @staticmethod
    def convert(quote: str, base: str, amount:str):

        if base == quote: # уведомляем об ошибке, если ввели одинаковые валюты, предварительно сравнив их
            raise ConvertionExeption(f'Вы ввели одинаковые валюты {base}')

        if float(amount) <= 0:
            raise ConvertionExeption(f'Кол-во валюты не может быть равно 0 или быть отрицательным')

        try: #проверяем на ошибки при введении сообщения
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Невозможно обработать валюту {quote}')

        try: #проверяем на ошибки при введении сообщения
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Невозможно обработать валюту {base}')

        try: #проверяем на ошибки при введении сообщения
            amount = float(amount)

        except ValueError:
            raise ConvertionExeption(f'Невозможно обработать колличество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_base = json.loads(r.content)[keys[base]]

        return (float(total_base)*float(amount))
