from pprint import pprint
from influxdb_client import InfluxDBClient
from dotenv import dotenv_values
from flask import Flask, render_template


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
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results


@app.route("/")
def hello():
    context = {"currencies": get_data()}
    return render_template("./index.html", **context)


if __name__ == "__main__":
    app.run(host="localhost", port=5005)
