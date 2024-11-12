import click
import asyncio
import httpx
import os
import random
from asyncio_pool import AioPool
from hashlib import sha256
from urllib.parse import urlparse
from tenacity import AsyncRetrying, RetryError, stop_after_attempt

RETRIES = 3
CONCURRENCY_SIZE = 2


class Downloader:
    def __init__(self, proxies=None, max_chunk_size=1000000):
        self.proxies = proxies
        # size in bytes, if any
        self._max_chunk_size = int(max_chunk_size * 1024 * 1024) if max_chunk_size else None

    async def get_size(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.head(url)
            size = int(response.headers["Content-Length"])
            return size

    async def download_range(self, url, start, end, output):
        headers = {"Range": f"bytes={start}-{end}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, headers=headers)

        with open(output, "wb") as f:
            for part in response.iter_bytes():
                f.write(part)
        click.echo(f"Finished: {output}")

    async def split_download(self, url, file_size, output):
        chunks = range(0, file_size, self._max_chunk_size)
        click.echo(f"Planned number of chunks: {len(chunks)}")
        calls = []
        async with AioPool(size=int(len(chunks) / 3)) as pool:
            for i, start in enumerate(chunks):
                partial_output = f"{output}.part{i}"
                result = await pool.spawn(
                    self.download_range(url, start, start + self._max_chunk_size - 1, partial_output)
                )
                calls.append(result)

        with open(output, "wb") as o:
            for i in range(len(chunks)):
                chunk_path = f"{output}.part{i}"

                with open(chunk_path, "rb") as s:
                    o.write(s.read())
                os.remove(chunk_path)

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
                            return await self.split_download(url, file_size, output_file_name)
                    async with httpx.AsyncClient(proxies=proxy_server) as client:
                        response = await client.get(url, follow_redirects=True)
                        if response.status_code == 200:
                            u = urlparse(url)
                            file_hash = sha256(url.encode("utf8")).hexdigest()
                            file_name = f"{os.path.basename(u.path)}_{file_hash}"
                            with open(f"/tmp/{file_name}", "wb") as f:
                                f.write(response.content)
        except RetryError:
            click.echo(f"Failed to fetch {url} after {RETRIES} tries")

    async def download_list(self, urls_file):
        calls = []
        with open(urls_file, "r") as f:
            async with AioPool(size=CONCURRENCY_SIZE) as pool:
                for item in f:
                    if item and "http" in item:
                        result = await pool.spawn(self.download(item.strip()))
                        calls.append(result)


@click.command()
@click.option("--url", help="File URL path to download")
@click.option("--url-list", help="File with URLs to download")
@click.option("--proxy", help="List of proxy servers", multiple=True)
@click.option("--size", default=None, help="Size limit (MB) for partial downloads", type=float)
def run(url, url_list, proxy, size):
    d = Downloader(proxy, size)
    run_app = None
    if url:
        run_app = d.download(url)
    elif url_list:
        run_app = d.download_list(url_list)
    if run_app:
        asyncio.run(run_app)
    else:
        click.echo("No option selected")


if __name__ == "__main__":
    run()
