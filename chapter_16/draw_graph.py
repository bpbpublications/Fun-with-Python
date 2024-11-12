import pandas as pd
import plotly.graph_objects as go
from influxdb_client import InfluxDBClient
from dotenv import dotenv_values
from dataclasses import make_dataclass


url = "http://localhost:8086"
config = dotenv_values(".env")
client = InfluxDBClient(url=url, token=config["API_KEY"], org=config["org"])
query_api = client.query_api()

query = """from(bucket: "coins")
  |> range(start: -100m)
  |> filter(fn: (r) => r._measurement == "price")"""

result = query_api.query(org=config["org"], query=query)

Point = make_dataclass("Point", [("Date", str), ("Value", float)])

results = []
for table in result:
    for record in table.records:
        results.append(Point(record.get_time(), record.get_value()))

df = pd.DataFrame(results)
fig = go.Figure([go.Scatter(x=df["Date"], y=df["Value"])])
fig.show()
