# sample

Get text sample file

* option 1

```bash
$ curl -L "https://en.wikipedia.org/wiki/Python_(programming_language)" | html2text > output.txt
```

* option 2

```bash
$ curl -L "https://en.wikipedia.org/wiki/Python_(programming_language)" -o source.html

$ pip install html2text
```

next convert

```python
with open('source.html', 'r') as f_read:
    data = html2text.html2text(f_read.read())
    with open('output.txt', 'w') as f_write:
        f_write.write(data)
```



```python
with open('output.txt', 'r') as f:
    data = f.read()

len(data.split('python')) - 1
```

validate

```bash
$ cat output.txt | grep python | wc -l
```

## regexp

```python
import re

DATES = re.compile(r"[A-Z]{1}[a-z]{3,}\s+[0-9]+, [0-9]+")
result = DATES.findall(data)

print(result)
['September 7, 2022']
```

## CSV

```python
import re
import csv

with open('output.txt', 'r') as f:
    data = f.read()

REF = re.compile(r"[0-9]+\..*?\[\"(.*?)\"\]\((http.*?)\)[\.\s]+(.*?)\.", re.M)
results = REF.findall(data)

with open('reference_links.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    for item in results:
        csv_writer.writerow(item)
```

* improved version

```python
with open('reference_links.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(results)
```

## regexp

```python
import re

DATES = re.compile(r"[A-Z]{1}[a-z]{3,}\s+[0-9]+, [0-9]+")
result = DATES.findall(data)

print(result)
['September 7, 2022']
```
