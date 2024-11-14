import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode


class ClientAmazon:

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-",
    }

    def parse_results(self, html_data):
        soup = BeautifulSoup(html_data, "html.parser")
        result = soup.find_all("div", {"class": "sg-col-inner"})

        for item in result:
            search_result = item.find_all("div", {"class": "s-search-results"})
            if search_result:
                break

        found_items = []
        for item in search_result.pop().find_all("div", {"class": "s-result-item"}):
            data = {}
            a_link = item.find_all("h2", {"class": "a-size-mini"})
            # item details
            if a_link:
                a_link = a_link.pop()
                data.update(
                    {
                        "url": "https://www.amazon.com{}".format(a_link.select("a")[0].attrs["href"]),
                        "title": a_link.select("a")[0].text.strip(),
                    }
                )
            # price
            price_box = item.find_all("div", {"data-cy": "price-recipe"})
            if price_box:
                price = price_box.pop().find_all("span", {"class": "a-offscreen"})
                if price:
                    data.update({"price": float(price.pop().text.replace("$", "").replace(",", ""))})
            if data:
                found_items.append(data)
        return found_items

    def get_cookies(self):
        url = "https://www.amazon.com"
        r = requests.get(url, headers=self.headers)
        return r.cookies

    def find_items(self, search_phrase):
        url = "https://www.amazon.com/s"

        params = {
            "crid": "20LMZ9KZCOSVL",
            "i": "aps",
            "ref": "nb_sb_ss_recent_1_0_recent",
            "url": "search-alias=aps",
            "k": search_phrase,
            "sprefix": f"{search_phrase},aps,193",
        }
        url += f"?{urlencode(params)}"
        cookies = self.get_cookies()

        result = requests.get(url, headers=self.headers, cookies=cookies)
        return self.parse_results(result.content)

    def product_details(self, product_url: str):
        cookies = self.get_cookies()
        r = requests.get(product_url, headers=self.headers)

        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find_all("span", {"class": "aok-offscreen"})
        if result:
            price = float(result[0].text.replace("$", "").replace(",", "").strip())
            return price
