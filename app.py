import os

from flask import Flask, jsonify
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)