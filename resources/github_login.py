from flask_restful import Resource
from oauth import github
from flask import g
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime

from models.user import UserModel


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(
            callback="http://localhost:3000/github/authorize"
        )


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()
        g.access_token = resp["access_token"]
        github_user = github.get("user")
        github_username = github_user.data["login"]

        user = UserModel.find_by_username(github_username)

        if not user:
            user = UserModel(username=github_username, password=None, email=None, activated=True)
            user.save_to_db()

        delta = datetime.timedelta(minutes=1)
        access_token = create_access_token(
            identity=user.id, fresh=True, expires_delta=delta
        )
        refresh_token = create_refresh_token(user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
