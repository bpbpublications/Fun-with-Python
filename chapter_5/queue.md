# simple queue

```python
import click
import queue


class Crawler:
    def __init__(self):
        self.urls_queue = queue.Queue()

    def _get_element(self):
        return self.urls_queue.get()

    def process(self):
        """Main method to start crawler and process"""
        pass
```

adding click

```python
import click
import os


@click.command()
@click.option("--source", help="CSV full file path", required=True)
def main(source):
    """Main entry point for processing URLs and start crawling."""
    assert os.path.exists(source), f"Given file {source} does not exist"
    c = Crawler()
    c.process()

if __name__ == '__main__':
    main()
```

* CSV file structure

```csv
https://www.python.org,1
https://www.python.org/community/forums/,2
https://www.reddit.com/r/learnpython/,2
https://en.wikipedia.org/wiki/Elvis_Presley,3
```

# process

## step 1

```python
import requests


def process(self):
    """Main method to start crawler and process"""
    while self.urls_queue.qsize() > 0:
        url, _ = self.urls_queue.get()
        response = requests.get(url)
        if response.status_code == 200:
            f_name = sha256(url.encode('utf-8')).hexdigest()
            output_file = f"/tmp/{f_name}.html"
            with open(output_file, "w") as f:
                f.write(response.text)
                click.echo(f"URL: {url} [saved] under {output_file}")
```

## step 2

```python
import time

SLEEP_TIME = 1

def process(self):
    """Main method to start crawler and process"""

    while self.urls_queue.qsize() > 0:
        url, number_of_retries = self.urls_queue.get()

        for try_item in range(int(number_of_retries)):
            click.echo(f"Number of retries: {try_item+1}/{number_of_retries}")
            response = requests.get(url)
            if response.status_code == 200:
                f_name = sha256(url.encode('utf-8')).hexdigest()
                output_file = f"/tmp/{f_name}.html"
                with open(output_file, "w") as f:
                    f.write(response.text)
                    click.echo(f"URL: {url} [saved] under {output_file}")
                    break
            else:
                click.echo(f"Fetching resource failed with status code {response.status_code} sleeping {SLEEP_TIME}s before retry")
                time.sleep(SLEEP_TIME)
```

## step 3

Non existing URL

```python
Traceback (most recent call last):
  File "/Users/hp/.virtualenvs/fun1/lib/python3.7/site-packages/urllib3/connection.py", line 175, in _new_conn
    (self._dns_host, self.port), self.timeout, **extra_kw
  File "/Users/hp/.virtualenvs/fun1/lib/python3.7/site-packages/urllib3/util/connection.py", line 72, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/socket.py", line 752, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno 8] nodename nor servname provided, or not known

During handling of the above exception, another exception occurred:

(...)

requests.exceptions.ConnectionError: HTTPConnectionPool(host='dummy.non-existing.url.com', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fd3705ba2d0>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known'))
```

### step 4

improve

```python
def process(self):
    """Main method to start crawler and process"""
    url_success = 0
    url_fails = 0
    while self.urls_queue.qsize() > 0:
        url, number_of_retries = self.urls_queue.get()


        for try_item in range(int(number_of_retries)):
            click.echo(f"Number of retries: {try_item+1}/{number_of_retries}")
            is_ok = False
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    f_name = sha256(url.encode('utf-8')).hexdigest()
                    output_file = f"/tmp/{f_name}.html"
                    with open(output_file, "w") as f:
                        f.write(response.text)
                        click.echo(f"URL: {url} [saved] under {output_file}")
                        url_success += 1
                        is_ok = True
                        break
            except Exception as e:
                click.echo(f"We failed to fetch URL {url} with exeception: {e}")

            click.echo(f"Fetching resource failed with status code {response.status_code} sleeping {SLEEP_TIME}s before retry")
            time.sleep(SLEEP_TIME)
        if not is_ok:
            url_fails += 1
    click.echo(f"We fetched {url_success} URLs with {url_fails} fails")
```


```python
def fetch_url(self, url, number_of_retries):
    for try_item in range(int(number_of_retries)):
        click.echo(f"Number of retries: {try_item+1}/{number_of_retries}")
        is_ok = False
        try:
            response = requests.get(url)
            if response.status_code == 200:
                f_name = sha256(url.encode('utf-8')).hexdigest()
                output_file = f"/tmp/{f_name}.html"
                with open(output_file, "w") as f:
                    f.write(response.text)
                    click.echo(f"URL: {url} [saved] under {output_file}")
                    url_success += 1
                    is_ok = True
                    return response.text
        except Exception as e:
            click.echo(f"We failed to fetch URL {url} with exeception: {e}")

        click.echo(f"Fetching resource failed with status code {response.status_code} sleeping {SLEEP_TIME}s before retry")
        time.sleep(SLEEP_TIME)

def process(self):
    """Main method to start crawler and process"""
    url_success = 0
    url_fails = 0
    while self.urls_queue.qsize() > 0:
        url, number_of_retries = self.urls_queue.get()
        content = self.fetch_url(self, url, number_of_retries)
        LINK.findall(content)

```

refactor more

```python
import re
from typing import Optional
from urllib.parse import urlparse

def fetch_url(self, url: str, number_of_retries: int) -> Optional[str]:
    click.echo(f"Fetching {url}")
    for try_item in range(int(number_of_retries)):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                f_name = sha256(url.encode('utf-8')).hexdigest()
                output_file = f"/tmp/{f_name}.html"
                with open(output_file, "w") as f:
                    f.write(response.text)
                    click.echo(f"URL: {url} [saved] under {output_file}")
                    return response.text
        except Exception as e:
            click.echo(f"We failed to fetch URL {url} with exeception: {e}")

        click.echo(f"Fetching resource failed with status code {response.status_code} sleeping {SLEEP_TIME}s before retry")
        time.sleep(SLEEP_TIME)

def process(self):
    """Main method to start crawler and process"""
    url_success = 0
    url_fails = 0
    while self.urls_queue.qsize() > 0:
        url, number_of_retries = self.urls_queue.get()
        base_url = urlparse(url)
        content = self.fetch_url(url, number_of_retries)
        results = LINK.findall(content)
        click.echo(f"Found {len(results)} links")
        for parsed_url in results:
            if parsed_url.startswith('/'):
                parsed_url = f"{base_url.scheme}://{base_url.netloc}{parsed_url}"
            if not parsed_url.startswith('http'):
                continue
            content = self.fetch_url(parsed_url, number_of_retries)
```
