import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, current_app
from extensions import cache
from werkzeug.exceptions import Forbidden

from models import SocialModel, UserModel
from schemas import (
    UserSocialsSchema,
    UserFacebookSchema,
    UserInstagramSchema,
    UserTiktokSchema,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint(
    "user_socials", __name__, description="Operations on user social medias"
)


@blp.route("/users/socials/batch/connect")
class BatchConnect(MethodView):
    @blp.arguments(UserSocialsSchema)
    @blp.response(201, UserSocialsSchema)
    @jwt_required()
    def post(self, socials_data):
        current_user_id = get_jwt_identity()["id"]
        social = SocialModel.query.filter_by(user_id=current_user_id).first()

        if not social:
            try:
                social = SocialModel(
                    user_id=current_user_id,
                    facebook=socials_data.get("facebook"),
                    instagram=socials_data.get("instagram"),
                    tiktok=socials_data.get("tiktok"),
                )
                social.add_user_social()
            except IntegrityError:
                abort(400, message="recipe with that title already exists")
            except SQLAlchemyError as e:
                abort(
                    500,
                    message=f"An error occurred while creating the recipe: {str(e)}",
                )
            print(social)
            return social

        else:
            try:
                social.update_user_social(socials_data)
                return UserSocialsSchema().dump(social), 200
            except Forbidden as e:
                abort(403, description=str(e))

            except Exception as e:
                abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/users/profile/socials")
class SocialList(MethodView):

    @blp.response(201, UserSocialsSchema)
    @cache.cached(timeout=60)
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()["id"]
            social = SocialModel.query.filter_by(user_id=current_user_id).first()
            if not social:
                return jsonify({"message": "user has no linked socials"}), 404

            serialized_user = UserSocialsSchema().dump(social)
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/users/<int:user_id_in_search>/socials")
class SocialDisplay(MethodView):

    @blp.response(201, UserSocialsSchema)
    @cache.cached(timeout=60 * 5)
    def get(self, user_id_in_search):

        try:
            user = UserModel.query.filter_by(id=user_id_in_search).first()
            social = SocialModel.query.filter_by(user_id=user_id_in_search).first()

            if not user:
                return jsonify({"message": "user does not exist"}), 404

            if not social:
                return jsonify({"message": "user has no linked socials"}), 404

            serialized_user = UserSocialsSchema().dump(social)
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/users/socials/facebook/connect")
class FacebookConnect(MethodView):

    @blp.arguments(UserFacebookSchema)
    @blp.response(201, UserSocialsSchema)
    @jwt_required()
    def post(self, socials_data):
        user_id = get_jwt_identity()["id"]
        social = SocialModel.query.filter_by(user_id=user_id).first()

        if not social:
            try:
                social = SocialModel(
                    user_id=user_id,
                    facebook=socials_data["facebook"],
                )
                social.add_user_social()
            except IntegrityError:
                abort(400, message="recipe with that title already exists")
            except SQLAlchemyError as e:
                abort(
                    500,
                    message=f"An error occurred while creating the recipe: {str(e)}",
                )
            return social

        else:
            try:

                social.update_user_social(socials_data)
                return UserSocialsSchema().dump(social), 200
            except Forbidden as e:
                abort(403, description=str(e))

            except Exception as e:
                abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/users/socials/instagram/connect")
class InstagramConnect(MethodView):

    @blp.arguments(UserInstagramSchema)
    @blp.response(201, UserSocialsSchema)
    @jwt_required()
    def post(self, socials_data):
        user_id = get_jwt_identity()["id"]
        social = SocialModel.query.filter_by(user_id=user_id).first()

        if not social:
            try:
                social = SocialModel(
                    user_id=user_id,
                    instagram=socials_data["instagram"],
                )
                social.add_user_social()
            except IntegrityError:
                abort(400, message="recipe with that title already exists")
            except SQLAlchemyError as e:
                abort(
                    500,
                    message=f"An error occurred while creating the recipe: {str(e)}",
                )
            return social

        else:
            try:

                social.update_user_social(socials_data)
                return UserSocialsSchema().dump(social), 200
            except Forbidden as e:
                abort(403, description=str(e))

            except Exception as e:
                abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/users/socials/tiktok/connect")
class TiktokConnect(MethodView):

    @blp.arguments(UserTiktokSchema)
    @blp.response(201, UserSocialsSchema)
    @jwt_required()
    def post(self, socials_data):
        user_id = get_jwt_identity()["id"]
        social = SocialModel.query.filter_by(user_id=user_id).first()

        if not social:
            try:
                social = SocialModel(
                    user_id=user_id,
                    tiktok=socials_data["tiktok"],
                )
                social.add_user_social()
            except IntegrityError:
                abort(400, message="recipe with that title already exists")
            except SQLAlchemyError as e:
                abort(
                    500,
                    message=f"An error occurred while creating the recipe: {str(e)}",
                )
            return social

        else:
            try:

                social.update_user_social(socials_data)
                return UserSocialsSchema().dump(social), 200
            except Forbidden as e:
                abort(403, description=str(e))

            except Exception as e:
                abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/users/socials/facebook/disconnect")
class FacebookDisconnect(MethodView):

    @blp.arguments(UserFacebookSchema)
    @blp.response(201, UserSocialsSchema)
    @jwt_required()
    def post(self, socials_data):
        user_id = get_jwt_identity()["id"]
        social = SocialModel.query.filter_by(user_id=user_id).first()

        if not social:
            return jsonify({"message": "user has no linked socials"}), 404
        else:
            try:
                social.facebook = None
                social.update_user_social(social.__dict__)
                return UserSocialsSchema().dump(social), 200
            except Forbidden as e:
                abort(403, description=str(e))

            except Exception as e:
                abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/users/socials/instagram/disconnect")
class InstagramDisconnect(MethodView):

    @blp.arguments(UserInstagramSchema)
    @blp.response(201, UserSocialsSchema)
    @jwt_required()
    def post(self, socials_data):
        user_id = get_jwt_identity()["id"]
        social = SocialModel.query.filter_by(user_id=user_id).first()

        if not social:
            return jsonify({"message": "user has no linked socials"}), 404
        else:
            try:
                social.instagram = None
                social.update_user_social(social.__dict__)
                return UserSocialsSchema().dump(social), 200
            except Forbidden as e:
                abort(403, description=str(e))

            except Exception as e:
                abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/users/socials/tiktok/disconnect")
class TiktokDisconnect(MethodView):

    @blp.arguments(UserTiktokSchema)
    @blp.response(201, UserSocialsSchema)
    @jwt_required()
    def post(self, socials_data):
        user_id = get_jwt_identity()["id"]
        social = SocialModel.query.filter_by(user_id=user_id).first()

        if not social:
            return jsonify({"message": "user has no linked socials"}), 404
        else:
            try:
                social.tiktok = None
                social.update_user_social(social.__dict__)
                return UserSocialsSchema().dump(social), 200
            except Forbidden as e:
                abort(403, description=str(e))

            except Exception as e:
                abort(500, description=f"Failed to update recipe information: {str(e)}")
