import json
import re
import requests
from db import DB

URL = "https://coinmarketcap.com/all/views/all/"
JSON_DATA = re.compile(r'<script\s+id="__NEXT_DATA__"\s+type="application/json">(.*?)</script>')


def main():
    db = DB()
    raw_data = requests.get(URL).text
    data = json.loads(JSON_DATA.findall(raw_data).pop())
    result = {}
    i = 0
    for item in json.loads(data["props"]["initialState"])["cryptocurrency"]["listingLatest"]["data"]:
        try:
            result[item[30]] = item[10]
            sql = f"""INSERT INTO currency(currency_code, currency_name) VALUES ('{item[30]}', '{item[10]}');"""
            db.commit(sql)
            i += 1
        except KeyError:
            pass
    return i


if __name__ == "__main__":
    no_items = main()
    print(f"Inserted {no_items} items")
