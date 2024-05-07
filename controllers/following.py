import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify

from models import (
    UserModel,
    FollowingModel,
)
from schemas import (
    UserFollowingSchema,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("following", __name__, description="Operations on following")


@blp.route("/users/follow/<int:user_id_to_follow>")
class FollowAUser(MethodView):

    @blp.response(201, UserFollowingSchema)
    @jwt_required()
    def post(self, user_id_to_follow):
        try:
            current_user_id = get_jwt_identity()["id"]
            user_to_follow = UserModel.query.filter_by(id=user_id_to_follow).first()
            has_followed = FollowingModel.query.filter_by(
                follower_id=current_user_id, followed_id=user_id_to_follow
            ).first()

            if current_user_id == user_id_to_follow:
                return jsonify({"message": "You cannot follow yourself"}), 403

            if user_to_follow is None:
                return jsonify({"message": "User does not exist"}), 404

            if has_followed:
                return jsonify({"message": "You have already followed the user"}), 403

            following = FollowingModel(
                follower_id=current_user_id,
                followed_id=user_id_to_follow,
            )

            following.add_following()

            return jsonify({"message": "You have successfully following the user"}), 200

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")


@blp.route("/users/unfollow/<int:user_id_to_follow>")
class UnfollowAUser(MethodView):

    @blp.response(201, UserFollowingSchema)
    @jwt_required()
    def post(self, user_id_to_follow):
        try:
            current_user_id = get_jwt_identity()["id"]
            user_to_follow = UserModel.query.filter_by(id=user_id_to_follow).first()
            has_followed = FollowingModel.query.filter_by(
                follower_id=current_user_id, followed_id=user_id_to_follow
            ).first()

            if not user_to_follow:
                return jsonify({"message": "User does not exist"}), 404

            if not has_followed:
                return jsonify({"message": "You have not followed the user yet"}), 403

            has_followed.delete_following()

            return jsonify({"message": "You have successfully unfollow the user"}), 200

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
