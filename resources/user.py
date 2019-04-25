from flask_restful import Resource
from flask import request, make_response, render_template
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
)
from models.user import UserModel
from schemas.user import UserSchema
from argon2 import PasswordHasher, exceptions
import datetime


user_schema = UserSchema()
ph = PasswordHasher()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        password = ph.hash(user_json["password"])
        user_json["password"] = password
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": "username exists"}, 400

        user.save_to_db()
        user.send_confirmation_email()
        return {"message": "you are now registered"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        user = UserModel.find_by_username(user_data.username)

        try:
            if user and ph.verify(user.password, user_data.password):
                delta = datetime.timedelta(hours=3)
                access_token = create_access_token(
                    identity=user.id, fresh=True, expires_delta=delta
                )
                refresh_token = create_refresh_token(user.id)
                return (
                    {"access_token": access_token, "refresh_token": refresh_token},
                    200,
                )
        except exceptions.VerifyMismatchError:
            return {"message": "invalid credentials"}, 401


class UserVerify(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "No user with id"}, 404
        if user.activated:
            return {"message": "user is already activated"}, 400

        user.activated = True
        user.save_to_db()
        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("email_confirm.html", email=user.email), 200, headers
        )

    @classmethod
    def post(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error": "User does not exist"}, 404

        if user.activated:
            return {"message": "user is already activated"}, 400
        try:

            user.send_confirmation_email()
            return {"message": "confirmation resend successful"}, 201

        except:
            return {"message": "confirmation resend fail"}, 500


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
