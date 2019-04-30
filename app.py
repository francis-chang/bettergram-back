import os
from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from db import db
from oauth import oauth
from ma import ma
from resources.user import UserRegister, UserLogin, UserVerify, TokenRefresh, User
from flask_jwt_extended import JWTManager
from resources.github_login import GithubLogin, GithubAuthorize

app = Flask(__name__)


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
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserVerify, "/confirmation/<int:user_id>")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(GithubLogin, "/login/github")
api.add_resource(GithubAuthorize, "/login/github/authorized")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    app.run(port=5000, debug=True)
