from pprint import pprint
from influxdb_client import InfluxDBClient
from dotenv import dotenv_values


url = "http://localhost:8086"
config = dotenv_values(".env")
client = InfluxDBClient(url=url, token=config["API_KEY"], org=config["org"])
query_api = client.query_api()

query = """from(bucket: "coins")
  |> range(start: -100m)
  |> filter(fn: (r) => r._measurement == "price")"""

result = query_api.query(org=config["org"], query=query)

results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))

pprint(results)
