import asyncio
from asyncio_pool import AioPool
from pprint import pprint

SITES = ["wikipedia.org", "google.com"]
PORTS = [443, 80, 25]


class MyScanner:
    def __init__(self):
        self.scanner_results = {}

    async def tcp_port_check(self, host, port):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            return [host, port, True]
        except Exception as e:
            print(e)
            return [host, port, False]

    async def start_scanning(self):
        calls = []
        results = {}
        async with AioPool(size=5) as pool:
            for site in SITES:
                for port in PORTS:
                    calls.append(await pool.spawn(self.tcp_port_check(site, port)))

        for r in calls:
            result = r.result()
            if result[0] not in self.scanner_results:
                self.scanner_results[result[0]] = {}
            self.scanner_results[result[0]][result[1]] = result[2]

    async def run(self):
        await self.start_scanning()
        pprint(self.scanner_results)


if __name__ == "__main__":
    scanner = MyScanner()
    asyncio.run(scanner.run())
