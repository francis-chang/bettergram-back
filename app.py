import os

from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from db import db

app = Flask(__name__)

load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)

api = Api(app)

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
