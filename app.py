import os
from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
import cloudinary

load_dotenv(".env", verbose=True)

from db import db
from oauth import oauth
from ma import ma
from resources.user import (
    UserRegister,
    UserLogin,
    UserVerify,
    TokenRefresh,
    User,
    UserLogout,
)
from resources.image import Image
from flask_jwt_extended import JWTManager, create_access_token
from resources.github_login import GithubLogin, GithubAuthorize
from blacklist import BLACKLIST


app = Flask(__name__)


app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)
app.secret_key = os.environ.get("SECRET_KEY")
jwt = JWTManager(app)

cloudinary.config(
    cloud_name=os.environ.get("CL_CLOUD_NAME"),
    api_key=os.environ.get("CL_API_KEY"),
    api_secret=os.environ.get("CL_API_SECRET"),
)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    new_token = create_access_token(
        identity=expired_token["identity"], fresh=False, expires_delta=False
    )
    return jsonify({"access_token": new_token}), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_bl(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserVerify, "/confirmation/<int:user_id>")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(GithubLogin, "/login/github")
api.add_resource(GithubAuthorize, "/login/github/authorized")
api.add_resource(Image, "/image")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    app.run(port=5000, debug=True)
