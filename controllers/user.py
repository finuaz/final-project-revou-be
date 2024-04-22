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
from flask import request, jsonify, current_app
from passlib.hash import pbkdf2_sha512

from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException, Forbidden

from db import db
from models import UserModel
from schemas import UserRegisterSchema, UserLoginSchema, UserGetProfileSchema

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/users/profile")
class UserProfile(MethodView):
    @jwt_required()
    @blp.response(200, schema=UserGetProfileSchema)
    def get(self):
        try:
            current_user_id = get_jwt_identity()["id"]
            user = UserModel.query.filter_by(id=current_user_id).first()
            if not user:
                abort(404, "User not found")

            serialized_user = UserGetProfileSchema().dump(user)
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/users/register")
class UserRegister(MethodView):

    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserRegisterSchema)
    def post(self, user_data):
        try:
            hashed_password = pbkdf2_sha512.hash(user_data["password"])
            user = UserModel(
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                reset_password_question=user_data["reset_password_question"],
                reset_password_answer=user_data["reset_password_answer"],
                password=hashed_password,
                role=None,
            )
            print(user)

            user.add_user()

        except IntegrityError:
            abort(400, message="User with that email already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the user: {str(e)}")
        return user


@blp.route("/users/login")
class UserLogin(MethodView):

    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha512.verify(user_data["password"], user.password):

            role = user.role.serialize() if user.role else None

            access_token = create_access_token(
                identity={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": role,
                },
                fresh=True,
            )
            refresh_token = create_refresh_token(
                identity={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": role,
                },
            )
            return {
                "message": "you are successfully login",
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            }, 200

        else:
            abort(401, "Invalid Credentials")


def get_user_id():
    jwt = get_jwt()
    return jwt.get("sub").get("id")
