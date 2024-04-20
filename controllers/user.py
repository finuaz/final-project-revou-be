from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import request, jsonify
from passlib.hash import pbkdf2_sha512

from db import db
from models import UserModel
from schemas import UserModelSchema

blprint = Blueprint("users", __name__, description="Operations on users")


@blprint.route("/register")
class UserRegister(MethodView):
    @blprint.arguments(UserModelSchema)
    @blprint.response(201, UserModelSchema)
    def post(self, user_data):
        try:
            hashed_password = pbkdf2_sha512.hash(user_data["password"])
            user = UserModel(
                username=user_data["username"],
                email=user_data["email"],
                name=user_data["name"],
                password=hashed_password,
                reset_password_question=None,
                reset_password_answer=None,
                image=None,
                role=None,
                bio=None,
                location=None,
                view_count=None,
            )
            print(user)

            user.add_user()

        except IntegrityError:
            abort(400, message="User with that email already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the user: {str(e)}")
        return user


@blprint.route("/login")
class UserLogin(MethodView):
    @blprint.arguments(UserModelSchema)
    @blprint.response(200, UserModelSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(email=user_data["email"]).first()

        if user and pbkdf2_sha512.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)


def get_user_id():
    jwt = get_jwt()
    return jwt.get("sub").get("id")
