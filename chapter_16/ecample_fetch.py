import requests
from pprint import pprint

url = f"https://price-api.crypto.com/price/v1/token-price/bitcoin"
result = requests.get(url, headers={"User-Agent": "Firefox"})
pprint(result.json())
