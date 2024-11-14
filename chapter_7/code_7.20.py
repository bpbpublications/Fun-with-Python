import os
import requests
from pprint import pprint

API_KEY = os.environ.get("API_KEY")
assert API_KEY, "variable API_KEY not specified"
URL = "https://api.livecoinwatch.com/credits"

response = requests.post(URL, headers={"x-api-key": API_KEY, "content-type": "application/json"}).json()
print("Credit status:")
pprint(response)
