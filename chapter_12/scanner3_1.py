import csv
from datetime import datetime


class MyScanner:
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
