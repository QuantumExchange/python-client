"""Get order book"""
import json

from client import Client

API_KEY = ""
API_SECRET = ""

client = Client(API_KEY, API_SECRET)

print("Get order book")

result = client.get_order_book("dai", "usdt")

print(json.dumps(result))

"""Place limit order"""

print("Place limit order")

result = client.create_market_order("buy", 5, "btc", "usdt")

print(json.dumps(result))