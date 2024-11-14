# sample

Get text sample file

* option 1

```bash
$ curl -L "https://en.wikipedia.org/wiki/Python_(programming_language)"  -o source.html
```

* extracting text

```python
import re
import csv

with open('source.html', 'r') as f_read:
    html_page = f_read.read()

cleaned_up_source = html_page.replace('\n', '')

REF = re.compile(r'<li.*?<a href="#cite_ref-AutoNT.*?class="external text"\s+href="(.*?)\".*?>"(.*?)"</a>.*?<i>(.*?)<\/i>', re.I)
CONTENT = re.compile(r'>References</(.*?)>Sources</', re.M)

content = CONTENT.findall(cleaned_up_source)
if content:
    result = REF.findall(content[0])
    with open('reference_links.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(results)
```

* install beautiful soup

```bash
$ pip install beautifulsoup4
```

bs4 parse

```python
import bs4
import csv
import re


with open('source.html', 'r') as f_read:
    html_page = f_read.read()

soup = BeautifulSoup(html_page, "html.parser")
cite_notes = soup.find_all('li', id=re.compile("cite_note-[0-9]+"))

with open('reference_links.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    for item in cite_notes:
        _link = item.find_all('a')[1]
        _link_href = _link.attrs['href']
        _link_text = _link.text.strip('"')
        csv_writer.writerow([_link_href, _link_text])
```
