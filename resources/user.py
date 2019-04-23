from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from schemas.user import UserSchema
from argon2 import PasswordHasher, exceptions

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

        return {"message": "you are now registered"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        try:
            if user and ph.verify(user.password, user_data.password):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
        except exceptions.VerifyMismatchError:
            return {"message": "invalid credentials"}, 401
