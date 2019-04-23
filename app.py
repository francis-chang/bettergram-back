import os

from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from db import db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from resources.user import UserRegister, UserLogin
from flask_jwt_extended import JWTManager

app = Flask(__name__)

load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)
app.secret_key = os.environ.get("SECRET_KEY")
jwt = JWTManager(app)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
