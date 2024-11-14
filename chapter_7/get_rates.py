import requests

url = "https://finage-currency-data-feed.p.rapidapi.com/convert"

querystring = {"from": "BTC", "to": "USD", "amount": "2", "apikey": "API_KEYUX0RG2F4BXCV5JJ50P0K3BLFQOS0Q0DP"}

headers = {
    "X-RapidAPI-Key": "645577fcd2mshf6e8a55ccb8a262p1661a5jsnf84fe3890743",
    "X-RapidAPI-Host": "finage-currency-data-feed.p.rapidapi.com",
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
