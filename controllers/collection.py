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
from extensions import cache


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

# blp = Blueprint("collections", __name__, description="Operations on collections")
