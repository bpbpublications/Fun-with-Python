import asyncio
import click
import csv
import httpx
import os
import re
from asyncio_pool import AioPool
from hashlib import sha256
from typing import Optional
from urllib.parse import urlparse

SLEEP_TIME = 1
LINK = re.compile(r"<a.*?href=[\"'](.*?)[\"']", re.I)
IMAGES = re.compile(r"<img.*?src=[\"'](.*?)[\"']", re.I)


class Crawler:
    def __init__(self, call_levels: int, concurency: int = None):
        self.urls_queue = asyncio.Queue()
        self.__call_levels = call_levels
        self.__concurrency = concurency

    async def load_content(self, file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.urls_queue.put_nowait(row)

        click.echo(f"After loaiding CSV content queue size id: {self.urls_queue.qsize()}")

    async def _get_element(self):
        return await self.urls_queue.get()

    async def fetch_url(self, url: str, number_of_retries: int) -> Optional[str]:
        click.echo(f"Fetching {url}")
        for try_item in range(int(number_of_retries)):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, follow_redirects=True)
                content_type = response.headers.get("Content-Type").split(";")[0]
                extension = content_type.split("/")[-1].lower()
                if response.status_code == 200:
                    f_name = sha256(url.encode("utf-8")).hexdigest()
                    output_file = f"/tmp/{f_name}.{extension}"
                    with open(output_file, "wb") as f:
                        data = response.content
                        f.write(data)
                        click.echo(f"URL: {url} [saved] under {output_file}")
                        return data.decode("utf-8")
            except Exception as e:
                click.echo(f"We failed to fetch URL {url} with exeception: {e}")

            click.echo(
                f"Fetching resource failed with status code {response.status_code} sleeping {SLEEP_TIME}s before retry"
            )
            if response.status_code != 404:
                await asyncio.sleep(SLEEP_TIME)

    async def process_item(self, url: str, number_of_retries: int, call_level: int = 1) -> asyncio.gather:
        base_url = urlparse(url)
        content = await self.fetch_url(url, number_of_retries)
        results = LINK.findall(content)
        parsed_images = IMAGES.findall(content)
        click.echo(f"Found {len(results)} links [level: {call_level}]")
        click.echo(f"Found {len(parsed_images)} images [level: {call_level}]")
        calls = []

        extracted_urls = filter(lambda x: x.startswith("/") or x.startswith("http"), results)
        parsed_images = filter(lambda x: x.startswith("/") or x.startswith("http"), parsed_images)

        for parsed_url in parsed_images:
            if parsed_url.startswith("/"):
                parsed_url = f"{base_url.scheme}://{base_url.netloc}{parsed_url}"
            calls.append(self.fetch_url(parsed_url, number_of_retries))
        if self.__concurrency:
            async with AioPool(size=self.__concurrency) as pool:
                for parsed_url in extracted_urls:
                    if parsed_url.startswith("/"):
                        parsed_url = f"{base_url.scheme}://{base_url.netloc}{parsed_url}"
                    if call_level < self.__call_levels:
                        await pool.spawn(self.process_item(parsed_url, number_of_retries, call_level + 1))
                    else:
                        await pool.spawn(self.fetch_url(parsed_url, number_of_retries))
        else:
            for parsed_url in extracted_urls:
                if parsed_url.startswith("/"):
                    parsed_url = f"{base_url.scheme}://{base_url.netloc}{parsed_url}"
                if call_level < self.__call_levels:
                    calls.append(self.process_item(parsed_url, number_of_retries, call_level + 1))
                else:
                    calls.append(self.fetch_url(parsed_url, number_of_retries))

        return await asyncio.gather(*calls)

    async def process(self):
        """Main method to start crawler and process"""
        calls = []
        while True:
            url, number_of_retries = await self.urls_queue.get()
            calls.append(self.process_item(url, number_of_retries))
            if self.urls_queue.empty():
                break
        await asyncio.gather(*calls)
        click.echo("Processing finished, exiting...")


async def main(source: str, level: int, pool: int):
    """Main entry point for processing URLs and start crawling."""
    assert os.path.exists(source), f"Given file {source} does not exist"
    c = Crawler(level, concurency=(pool if pool > 0 else None))
    await c.load_content(source)
    await c.process()


@click.command()
@click.option("--source", help="CSV full file path", required=True)
@click.option("--level", help="Crawling depth level", type=int, required=False, default=5)
@click.option("--pool", help="Crawling pool size", type=int, required=False, default=-1)
def run(source, level, pool):
    asyncio.run(main(source, level, pool))


if __name__ == "__main__":
    run()
