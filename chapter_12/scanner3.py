import aioping
import asyncio
import coloredlogs
import csv
import click
import httpx
import logging
import os
import yaml
from asyncio_pool import AioPool
from datetime import datetime
from pprint import pformat
from urllib.parse import urlparse


class MyScanner:
    def __init__(self, config_fpath):
        with open(config_fpath, "rb") as f:
            self._config = yaml.load(f.read(), Loader=yaml.Loader)
        print(self._config)
        self.scanner_results = {}

    def hostname(self, url):
        parsed_uri = urlparse(url)
        return parsed_uri.netloc

    async def tcp_port_check(self, host, port):
        try:
            fqdn = self.hostname(host)
            logging.debug(f"host: {fqdn}, port: {port}")
            func = asyncio.open_connection(fqdn, port)
            reader, writer = await asyncio.wait_for(func, timeout=3)
            return [fqdn, str(port), True]
        except Exception as e:
            logging.error(e)
            return [fqdn, str(port), False]

    async def start_scanning(self):
        calls = []
        results = {}
        async with AioPool(size=5) as pool:
            for item, items in self._config.get("sites", {}).items():

                for port in items["ports"]:
                    calls.append(await pool.spawn(self.tcp_port_check(items["url"], port)))
                calls.append(await pool.spawn(self.ping_host(items["url"])))
                calls.append(await pool.spawn(self.check_status(items["url"])))

        for r in calls:
            result = r.result()
            if result[0] not in self.scanner_results:
                self.scanner_results[result[0]] = {}
            self.scanner_results[result[0]][result[1]] = result[2]
        for site, results in self.scanner_results.items():
            self.dump_to_csv(site, results)

    def dump_to_csv(self, item, data):
        fname = f"/var/tmp/{item}.csv"
        headers = sorted([k for k in data.keys()])
        headers.insert(0, "date")
        data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%s")
        if not os.path.exists(fname):
            with open(fname, "a") as f:
                csv_out = csv.writer(f)
                csv_out.writerow(headers)
        with open(fname, "a") as f:
            csv_out = csv.writer(f)
            csv_out.writerow([data.get(k) for k in headers])

    async def run(self):
        await self.start_scanning()
        logging.debug(f"result: {pformat(self.scanner_results)}")

    async def ping_host(self, host) -> float:
        fqdn = self.hostname(host)
        delay = await aioping.ping(fqdn) * 1000
        logging.debug(f"Response time {delay} ms")
        return [fqdn, "ping", delay]

    async def check_status(self, url) -> bool:
        fqdn = self.hostname(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            status = response.status_code == 200 and len(response.text) >= 50
            logging.debug(f"Site status: {status}")
            return [fqdn, "status", status]


@click.command()
@click.option("--config", help="Config file path", required=True)
def main(config):
    coloredlogs.install(level=logging.DEBUG)
    scanner = MyScanner(config)
    asyncio.run(scanner.run())


if __name__ == "__main__":
    main()
