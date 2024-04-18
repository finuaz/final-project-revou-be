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
from passlib.hash import pbkdf2_sha256

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
            print("halo")
            hashed_password = pbkdf2_sha256.hash(user_data["password"])
            user = UserModel(
                username=user_data["username"],
                password=hashed_password,
                email=user_data["email"],
                name=user_data["name"],
            )
            db.session.add(user)
            db.session.commit()
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

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)


def get_user_id():
    jwt = get_jwt()
    return jwt.get("sub").get("id")
