from bs4 import BeautifulSoup

with open("/tmp/result.html", "rb") as f:
    soup = BeautifulSoup(f.read(), "html.parser")


def has_class_but_no_id(tag):
    return tag and getattr(tag, "has_attr", None) and tag.has_attr("class") and not tag.has_attr("id")


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
        data.update({"price": price.pop().text})
    if data:
        found_items.append(data)


from pprint import pprint

pprint(found_items)
