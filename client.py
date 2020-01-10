"""
Quantum Exchange API client
"""

import requests
import hmac
import time
import hashlib

URL_PREFIX = 'https://api.quantum.exchange'


def _nonce():
    return int(round(time.time() * 1000000))


def generate_auth_headers(api_key, api_secret, method, path, body):
    nonce = str(_nonce())
    signature = "{}{}{}{}".format(nonce, method, path, body)
    h = hmac.new(api_secret.encode('utf8'), signature.encode('utf8'), hashlib.sha384)
    signature = h.hexdigest()

    return {
        "QUANTUM_API_KEY": api_key,
        "QUANTUM_API_SIGNATURE": signature,
        "QUANTUM_API_NONCE": nonce
    }


class Client:

    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret

    def call_post(self, path, data):
        headers = generate_auth_headers(self.api_key, self.api_secret, "POST", path, data)
        x = requests.post(URL_PREFIX + path, json=data, headers=headers)
        return x.json()

    def create_limit_order(self, action,  amount, price, asset, currency):
        return self.call_post("/v1/createOrder", {'action': action, 'amount': amount, 'price': price, 'asset': asset,
                                                  'currency': currency, 'type': 'limit'})

    def create_market_order(self, action, amount, asset, currency):
        return self.call_post("/v1/createOrder", {'action': action, 'amount': amount, 'asset': asset,
                                                  'currency': currency, 'type': 'market'})

    def cancel_all_orders(self,  asset, currency):
        return self.call_post("/v1/order/cancel/all", {'asset': asset, 'currency': currency})

    @staticmethod
    def get_order_book(asset, currency):
        x = requests.get(URL_PREFIX + f'/v1/order_book/{asset}/{currency}')
        return x.json()
