import json
import re
import requests
from pprint import pprint

URL = "https://coinmarketcap.com/all/views/all/"
JSON_DATA = re.compile(r'<script\s+id="__NEXT_DATA__"\s+type="application/json">(.*?)</script>')


def main():
    raw_data = requests.get(URL).text
    data = json.loads(JSON_DATA.findall(raw_data).pop())
    result = {}
    for item in json.loads(data["props"]["initialState"])["cryptocurrency"]["listingLatest"]["data"]:
        try:
            result[item[30]] = item[10]
        except KeyError:
            pass
    return result


if __name__ == "__main__":
    pprint(main())
