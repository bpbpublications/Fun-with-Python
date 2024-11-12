import math
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pprint import pprint
from influxdb_client import InfluxDBClient
from dotenv import dotenv_values
from flask import Flask, render_template, Response
from dataclasses import make_dataclass
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from datetime import datetime

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


def forecast_data(df):
    forecast_col = "Value"
    df.fillna(value=-99999, inplace=True)
    forecast_size = int(math.ceil(0.03 * len(df)))
    df["Date"] = df["Date"].apply(lambda x: x.timestamp())
    df["label"] = df[forecast_col].shift(-forecast_size)

    x = np.array(df.drop(["label"], axis=1))
    print(x)
    x = preprocessing.power_transform(x)
    x_lately = x[-forecast_size:]
    x = x[:-forecast_size]

    df.dropna(inplace=True)

    y = np.array(df["label"])
    x_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    clf = Ridge(alpha=1.0)
    clf.fit(x_train, y_train)
    confidence = clf.score(X_test, y_test)

    forecast_set = clf.predict(x_lately)
    df["Forecast"] = np.nan
    last_date = df.iloc[-1].name
    last_unix = last_date
    one_day = 60  # 1 minute in seconds
    next_unix = last_unix + one_day

    for i in forecast_set:
        next_date = datetime.fromtimestamp(next_unix)
        next_unix += one_day
        df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]


@app.route("/graph")
def graph():
    results = get_data()
    df = pd.DataFrame(results)
    forecast_data(df)
    df["Date"] = pd.to_datetime(df["Date"], unit="s")
    fig = go.Figure([go.Scatter(x=df["Date"], y=df["Value"])])
    img_bytes = fig.to_image(format="png")
    return Response(img_bytes, mimetype="image/png")


@app.route("/")
def hello():
    context = {}
    return render_template("./index.html", **context)


if __name__ == "__main__":
    app.run(host="localhost", port=5005)
