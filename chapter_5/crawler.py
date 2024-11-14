import click
import csv
import os
import re
import requests
import time
import queue
from hashlib import sha256
from typing import Optional
from urllib.parse import urlparse

SLEEP_TIME = 1
LINK = re.compile(r"<a.*?href=[\"'](.*?)[\"']", re.I)


class Crawler:
    def __init__(self):
        self.urls_queue = queue.Queue()

    def load_content(self, file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.urls_queue.put(row)

        click.echo(f"After loaiding CSV content queue size id: {self.urls_queue.qsize()}")

    def _get_element(self):
        return self.urls_queue.get()

    def fetch_url(self, url: str, number_of_retries: int) -> Optional[str]:
        click.echo(f"Fetching {url}")
        for try_item in range(int(number_of_retries)):
            try:
                response = requests.get(url)
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
                if parsed_url.startswith("/"):
                    parsed_url = f"{base_url.scheme}://{base_url.netloc}{parsed_url}"
                if not parsed_url.startswith("http"):
                    continue
                content = self.fetch_url(parsed_url, number_of_retries)


@click.command()
@click.option("--source", help="CSV full file path", required=True)
def main(source):
    """Main entry point for processing URLs and start crawling."""
    assert os.path.exists(source), f"Given file {source} does not exist"
    c = Crawler()
    c.load_content(source)
    c.process()


if __name__ == "__main__":
    main()
