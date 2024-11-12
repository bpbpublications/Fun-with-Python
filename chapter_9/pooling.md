# installation

```
$ pip install asyncio_pool
```


# proxy

```bash
$ python proxy_service.py

Now serving at 9097
```

## use

```bash
$ curl -x http://localhost:9097 http://google.com
```

single URL

```bash
$ python download_with_proxy.py --url https://www.wikipedia.org

Fetching: https://www.wikipedia.org, proxy: None
```

failed with SSL proxy

```bash
$ python download_with_proxy.py --url-list example_files_list.txt  --proxy=http://localhost:9097

Fetching: https://www.wikipedia.org/portal/wikipedia.org/assets/img/sprite-8bb90067.svg, proxy: {'all://': 'http://localhost:9097'}
```

proxy server error

```bash
127.0.0.1 - - [20/Oct/2023 22:17:21] code 501, message Unsupported method ('CONNECT')
127.0.0.1 - - [20/Oct/2023 22:17:21] "CONNECT www.wikipedia.org:443 HTTP/1.1" 501 -
```

# pproxy

```bash
$ pip install pproxy
```

starting

```bash
$ pproxy

Serving on :8080 by http,socks4,socks5
```

ok with pproxy

```bash
$ python download_with_proxy.py --url-list example_files_list.txt  --proxy=http://localhost:8080

Fetching: https://www.wikipedia.org/portal/wikipedia.org/assets/img/sprite-8bb90067.svg, proxy: {'all://': 'http://localhost:8080'}
```

# in chunks

```bash
$ python download_in_chunks.py

Planned number of chunks: 28
Finished: /tmp/Python-3.12.0.tgz.part8
Finished: /tmp/Python-3.12.0.tgz.part2
Finished: /tmp/Python-3.12.0.tgz.part6
Finished: /tmp/Python-3.12.0.tgz.part1
Finished: /tmp/Python-3.12.0.tgz.part0
Finished: /tmp/Python-3.12.0.tgz.part5
Finished: /tmp/Python-3.12.0.tgz.part4
Finished: /tmp/Python-3.12.0.tgz.part7
Finished: /tmp/Python-3.12.0.tgz.part3
Finished: /tmp/Python-3.12.0.tgz.part10
Finished: /tmp/Python-3.12.0.tgz.part9
Finished: /tmp/Python-3.12.0.tgz.part12
Finished: /tmp/Python-3.12.0.tgz.part11
Finished: /tmp/Python-3.12.0.tgz.part17
Finished: /tmp/Python-3.12.0.tgz.part16
Finished: /tmp/Python-3.12.0.tgz.part15
Finished: /tmp/Python-3.12.0.tgz.part13
Finished: /tmp/Python-3.12.0.tgz.part14
Finished: /tmp/Python-3.12.0.tgz.part18
Finished: /tmp/Python-3.12.0.tgz.part19
Finished: /tmp/Python-3.12.0.tgz.part21
Finished: /tmp/Python-3.12.0.tgz.part20
Finished: /tmp/Python-3.12.0.tgz.part22
Finished: /tmp/Python-3.12.0.tgz.part24
Finished: /tmp/Python-3.12.0.tgz.part23
Finished: /tmp/Python-3.12.0.tgz.part25
Finished: /tmp/Python-3.12.0.tgz.part27
Finished: /tmp/Python-3.12.0.tgz.part26
```

download result

```bash
$ ls -l /tmp/Python-3.12.0.tgz

-rw-r--r--  1 hubertpiotrowski  wheel  27195214 Oct 22 15:21 /tmp/Python-3.12.0.tgz
```

uncompress

```bash
$ tar zxvf /tmp/Python-3.12.0.tgz

x Python-3.12.0/
x Python-3.12.0/Grammar/
x Python-3.12.0/Grammar/python.gram
x Python-3.12.0/Grammar/Tokens
x Python-3.12.0/Parser/
x Python-3.12.0/Parser/tokenizer.h
x Python-3.12.0/Parser/pegen.c
x Python-3.12.0/Parser/string_parser.h
(...)
```

checksum

```bash
$ md5sum /tmp/Python-3.12.0.tgz

d6eda3e1399cef5dfde7c4f319b0596c  /tmp/Python-3.12.0.tgz
```

## file size

```bash
$ python download_pool_and_chunks.py --url-list example_big_files_list.txt --size 1
```

output

```
Fetching: https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz, proxy: None
1048576
Fetching: https://www.php.net/distributions/php-8.1.24.tar.gz, proxy: None
1048576
File size: 27195214
Planned number of chunks: 26
File size: 18692939
Planned number of chunks: 18
Finished: Python-3.12.0.tgz.part7
Finished: Python-3.12.0.tgz.part6
Finished: Python-3.12.0.tgz.part5
Finished: Python-3.12.0.tgz.part1
Finished: Python-3.12.0.tgz.part2
Finished: Python-3.12.0.tgz.part4
Finished: Python-3.12.0.tgz.part0
Finished: php-8.1.24.tar.gz.part4
Finished: php-8.1.24.tar.gz.part2
Finished: php-8.1.24.tar.gz.part3
Finished: Python-3.12.0.tgz.part3
Finished: Python-3.12.0.tgz.part9
Finished: Python-3.12.0.tgz.part10
Finished: php-8.1.24.tar.gz.part0
Finished: Python-3.12.0.tgz.part12
Finished: Python-3.12.0.tgz.part11
Finished: Python-3.12.0.tgz.part8
Finished: Python-3.12.0.tgz.part14
Finished: php-8.1.24.tar.gz.part6
Finished: php-8.1.24.tar.gz.part7
Finished: Python-3.12.0.tgz.part17
Finished: Python-3.12.0.tgz.part20
Finished: php-8.1.24.tar.gz.part8
Finished: Python-3.12.0.tgz.part21
Finished: php-8.1.24.tar.gz.part10
Finished: Python-3.12.0.tgz.part15
Finished: Python-3.12.0.tgz.part22
Finished: Python-3.12.0.tgz.part23
Finished: php-8.1.24.tar.gz.part5
Finished: Python-3.12.0.tgz.part24
Finished: php-8.1.24.tar.gz.part1
Finished: Python-3.12.0.tgz.part25
Finished: php-8.1.24.tar.gz.part13
Finished: Python-3.12.0.tgz.part13
Finished: php-8.1.24.tar.gz.part11
Finished: php-8.1.24.tar.gz.part14
Finished: php-8.1.24.tar.gz.part15
Finished: Python-3.12.0.tgz.part19
Finished: php-8.1.24.tar.gz.part16
Finished: Python-3.12.0.tgz.part16
Finished: php-8.1.24.tar.gz.part17
Finished: php-8.1.24.tar.gz.part9
Finished: php-8.1.24.tar.gz.part12
Finished: Python-3.12.0.tgz.part18
```


fixed bugs

```Python
async def download(self, url):
    """Fetch URL resource with retry"""
    try:
        async for attempt in AsyncRetrying(stop=stop_after_attempt(RETRIES)):
            with attempt:
                proxy_server = None
                if self.proxies:
                    proxy_server = {
                        "all://": random.choice(self.proxies),
                    }
                click.echo(f"Fetching: {url}, proxy: {proxy_server}")
                if self._max_chunk_size:
                    file_size = await self.get_size(url)
                    click.echo(f"File size: {file_size}")
                    if file_size >= self._max_chunk_size:
                        _url = urlparse(url)
                        output_file_name = _url.path.split("/")[-1].strip()
                        output_file_name = f"/tmp/{output_file_name}"
                        return await self.split_download(url, file_size, output_file_name)
                async with httpx.AsyncClient(proxies=proxy_server) as client:
                    response = await client.get(url, follow_redirects=True)
                    if response.status_code == 200:
                        u = urlparse(url)
                        file_hash = sha256(url.encode("utf8")).hexdigest()
                        file_name = f"{os.path.basename(u.path)}_{file_hash}"
                        with open(f"/tmp/{file_name}", "wb") as f:
                            f.write(response.content)
```
