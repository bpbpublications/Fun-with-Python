import asyncio
import click
import csv
import httpx
import os
import re
from hashlib import sha256
from typing import Optional
from urllib.parse import urlparse

SLEEP_TIME = 1
LINK = re.compile(r"<a.*?href=[\"'](.*?)[\"']", re.I)


class Crawler:
    def __init__(self):
        self.urls_queue = asyncio.Queue()

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
                if response.status_code == 200:
                    f_name = sha256(url.encode("utf-8")).hexdigest()
                    output_file = f"/tmp/{f_name}.html"
                    with open(output_file, "w") as f:
                        f.write(response.text)
                        click.echo(f"URL: {url} [saved] under {output_file}")
                        return response.text
            except Exception as e:
                click.echo(f"We failed to fetch URL {url} with exeception: {e}")

            click.echo(
                f"Fetching resource failed with status code {response.status_code} sleeping {SLEEP_TIME}s before retry"
            )
            await asyncio.sleep(SLEEP_TIME)

    async def process(self):
        """Main method to start crawler and process"""
        url_success = 0
        url_fails = 0
        while True:
            url, number_of_retries = await self.urls_queue.get()
            base_url = urlparse(url)
            content = await self.fetch_url(url, number_of_retries)
            results = LINK.findall(content)
            click.echo(f"Found {len(results)} links")
            calls = []
            for parsed_url in results:
                if parsed_url.startswith("/"):
                    parsed_url = f"{base_url.scheme}://{base_url.netloc}{parsed_url}"
                if not parsed_url.startswith("http"):
                    continue
                calls.append(self.fetch_url(parsed_url, number_of_retries))
            await asyncio.gather(*calls)
            if self.urls_queue.empty():
                break
        click.echo("Processing finished, exiting...")


async def main(source):
    """Main entry point for processing URLs and start crawling."""
    assert os.path.exists(source), f"Given file {source} does not exist"
    c = Crawler()
    await c.load_content(source)
    await c.process()


@click.command()
@click.option("--source", help="CSV full file path", required=True)
def run(source):
    asyncio.run(main(source))


if __name__ == "__main__":
    run()
