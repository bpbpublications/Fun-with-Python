import io
import yaml
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, make_response, Response
from flask import render_template, send_file
from urllib.parse import urlparse
from matplotlib.figure import Figure

app = Flask(__name__)


def create_img(x, y, title="", xlabel="Date", ylabel="Value", dpi=100):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y, color="tab:red")
    return fig


CONFIG_FILE_PATH = "../config.yaml"
with open(CONFIG_FILE_PATH, "rb") as f:
    CONFIG = yaml.load(f.read(), Loader=yaml.Loader)


def get_fqdn(site):
    url = CONFIG["sites"][site]["url"]
    parsed_uri = urlparse(url)
    return parsed_uri.netloc


@app.route("/")
def list_of_result():
    return render_template("index.html", config=CONFIG, title="Main page")


@app.route("/results/<site>")
def scanning_results(site):
    data = CONFIG["sites"][site]
    return render_template("site_results.html", data=data, site=site, title="List of scanned elements")


@app.route("/port_scanning_results/<site>/<port>")
def port_scanning_results(site, port):
    data = CONFIG["sites"][site]
    fqdn = get_fqdn(site)
    df = pd.read_csv(f"/var/tmp/{fqdn}.csv", parse_dates=["date"], index_col="date")
    history_items = zip((df.index.values), list(df["ping"].array))
    return render_template("port_scanning_results.html", site=site, port=port, title="Details", items=history_items)


@app.route("/history/<site>/<scanned_item>")
def history(site, scanned_item):
    fqdn = get_fqdn(site)
    df = pd.read_csv(f"/var/tmp/{fqdn}.csv", parse_dates=["date"], index_col="date")
    fig = create_img(df.index, df[scanned_item], title=f"Results of scanning {scanned_item}")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")
