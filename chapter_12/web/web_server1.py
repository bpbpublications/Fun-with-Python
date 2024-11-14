import yaml
from flask import Flask

app = Flask(__name__)

CONFIG_FILE_PATH = "../config.yaml"
with open(CONFIG_FILE_PATH, "rb") as f:
    CONFIG = yaml.load(f.read(), Loader=yaml.Loader)


@app.route("/")
def list_of_result():
    return "hello"
