import os

from flask import Flask, jsonify
from flask_restful import Api
from db import db

app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)