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
from flask import jsonify, current_app
from passlib.hash import pbkdf2_sha512


from werkzeug.exceptions import Forbidden

from models import UserModel
from schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserGetProfileSchema,
    UserUpdateInfoSchema,
    UserUpdateImageSchema,
    UserResetPasswordSchema,
    UserDeletionSchema,
)

blp = Blueprint("users", __name__, description="Operations on users")


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


@blp.route("/users/profile")
class UserGetOwnProfile(MethodView):
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


@blp.route("/users/<string:username_in_search>")
class GetProfileByUsername(MethodView):

    @blp.response(200, schema=UserGetProfileSchema)
    def get(self, username_in_search):
        try:

            user = UserModel.query.filter_by(username=username_in_search).first()

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


@blp.route("/users/<int:user_id_in_search>")
class GetProfileById(MethodView):

    @blp.response(200, schema=UserGetProfileSchema)
    def get(self, user_id_in_search):
        try:

            user = UserModel.query.filter_by(id=user_id_in_search).first()

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


@blp.route("/users/update-info")
class UserUpdateInfo(MethodView):
    @jwt_required()
    @blp.arguments(UserUpdateInfoSchema)
    @blp.response(201, UserUpdateInfoSchema)
    def put(self, user_data):

        try:
            user_id = get_jwt_identity()["id"]

            user = UserModel.query.filter_by(id=user_id).first()

            user.update_user(user_data)

            return UserUpdateInfoSchema().dump(user), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to update user information: {str(e)}")


@blp.route("/users/update-image")
class UserUpdateImage(MethodView):

    @jwt_required()
    @blp.arguments(UserUpdateImageSchema)
    @blp.response(201, UserUpdateImageSchema)
    def put(self, user_data):
        try:
            user_id = get_jwt_identity()["id"]

            user = UserModel.query.filter_by(id=user_id).first()

            user.update_user(user_data)

            return UserUpdateImageSchema().dump(user), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to update user information: {str(e)}")


@blp.route("/users/reset-password")
class UserResetPassword(MethodView):

    @jwt_required()
    @blp.arguments(UserResetPasswordSchema)
    @blp.response(200, UserResetPasswordSchema)
    def put(self, user_data):
        user_id = get_jwt_identity()["id"]

        user = UserModel.query.filter_by(id=user_id).first()

        # Verify current password before proceeding with the reset
        if user and pbkdf2_sha512.verify(user_data["password"], user.password):
            if user.reset_password_answer == user_data["reset_password_answer"]:
                try:
                    # Update user's password with the new password
                    user.update_password(pbkdf2_sha512.hash(user_data["new_password"]))

                    return UserResetPasswordSchema().dump(user), 200

                except Forbidden as fe:
                    abort(403, description=str(fe))

                except Exception as e:
                    abort(500, description=f"Failed to reset user's password: {str(e)}")
            else:
                abort(400, description="Incorrect reset password answer")
        else:
            abort(400, description="Incorrect current password")


@blp.route("/users/delete")
class UserDelete(MethodView):

    @jwt_required()
    @blp.arguments(UserDeletionSchema)
    @blp.response(204, "your user has been deleted")
    def delete(self, user_data):

        user_id = get_jwt_identity()["id"]

        user = UserModel.query.filter_by(id=user_id).first()

        if user and pbkdf2_sha512.verify(user_data["password"], user.password):
            try:

                user.delete_user()
                return jsonify({"message": "your user has been deleted"}), 200

            except Forbidden as fe:
                abort(403, description=str(fe))

            except Exception as e:
                abort(500, description=f"Failed to delete user: {str(e)}")


def get_user_id():
    jwt = get_jwt()
    return jwt.get("sub").get("id")
