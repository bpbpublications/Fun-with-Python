import pandas as pd
import plotly.graph_objects as go
from pprint import pprint
from influxdb_client import InfluxDBClient
from dotenv import dotenv_values
from flask import Flask, render_template, Response
from dataclasses import make_dataclass


url = "http://localhost:8086"
config = dotenv_values(".env")
client = InfluxDBClient(url=url, token=config["API_KEY"], org=config["org"])
query_api = client.query_api()


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def get_data():
    query = """from(bucket: "coins")
    |> range(start: -200m)
    |> filter(fn: (r) => r._measurement == "price")"""

    result = query_api.query(org=config["org"], query=query)
    Point = make_dataclass("Point", [("Date", str), ("Value", float)])
    results = []
    for table in result:
        for record in table.records:
            results.append(Point(record.get_time(), record.get_value()))

    return results


@app.route("/graph")
def graph():
    results = get_data()
    df = pd.DataFrame(results)
    fig = go.Figure([go.Scatter(x=df["Date"], y=df["Value"])])
    img_bytes = fig.to_image(format="png")
    return Response(img_bytes, mimetype="image/png")


@app.route("/")
def hello():
    context = {}
    return render_template("./index.html", **context)


if __name__ == "__main__":
    app.run(host="localhost", port=5005)
