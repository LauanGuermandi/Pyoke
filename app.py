from flask import Flask
from controller.Pyoke import Pyoke

app = Flask(__name__)

app.config["APPLICATION_ROOT"] = "/api/v1"


@app.route("/analyze")
def analyze():
    return Pyoke()

