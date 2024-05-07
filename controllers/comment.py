import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, current_app, request
from db import db

from werkzeug.exceptions import Forbidden

from models import RecipeModel, UserModel, CommentModel

from utils import get_comments


from schemas import CommentSchema, RecipeSchema, RecipePlusPlusSchema


logging.basicConfig(level=logging.INFO)


blp = Blueprint("comments", __name__, description="Operations on comments")


@blp.route("/recipes/comment/<int:recipe_in_search>")
class AddCommentToRecipe(MethodView):
    @blp.response(201, CommentSchema)
    @jwt_required()
    def post(self, recipe_in_search):
        try:
            current_user_id = get_jwt_identity()["id"]
            comment_message = request.json.get("message")
            # existing_comment = CommentModel.query.filter_by(
            #     recipe_id=recipe_in_search, user_id=current_user_id
            # ).first()
            recipe = RecipeModel.query.filter_by(id=recipe_in_search).first()

            if not recipe:
                abort(404, message="Recipe not found")

            if not comment_message:
                abort(400, message="comment message is required")

            # if existing_comment:

            #     existing_comment.message = comment_message
            #     existing_comment.update_comment(
            #         comment_data={"message": comment_message}
            #     )

            #     response_data = {
            #         "id": existing_comment.id,
            #         "user_id": existing_comment.user_id,
            #         "recipe_id": existing_comment.recipe_id,
            #         "message": existing_comment.message,
            #     }
            #     return jsonify(response_data)

            comment = CommentModel(
                recipe_id=recipe_in_search,
                user_id=current_user_id,
                message=comment_message,
            )

            comment.add_comment()

            comment.message = comment.message

            comments = get_comments(recipe_in_search)

            serialized_comment = CommentSchema().dump(comment)
            return jsonify(serialized_comment), 200

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")


@blp.route("/recipes/comment/<int:recipe_in_search>/edit/<int:comment_id_in_search>")
class UpdateCommentOnRecipe(MethodView):
    @blp.response(201, CommentSchema)
    @jwt_required()
    def put(self, recipe_in_search, comment_id_in_search):
        try:
            current_user_id = get_jwt_identity()["id"]
            comment_message = request.json.get("message")
            existing_comment = CommentModel.query.filter_by(
                id=comment_id_in_search
            ).first()
            recipe = RecipeModel.query.filter_by(id=recipe_in_search).first()

            if not recipe:
                abort(404, message="Recipe not found")

            if existing_comment.user_id != current_user_id:
                return (
                    jsonify({"message": "you are not authorized to edit this comment"}),
                    403,
                )

            if not comment_message:
                abort(400, message="comment message is required")

            if not existing_comment:
                return jsonify({"message": "the comment is not found"}), 404

            existing_comment.message = comment_message
            existing_comment.update_comment(comment_data={"message": comment_message})

            response_data = {
                "id": existing_comment.id,
                "user_id": existing_comment.user_id,
                "recipe_id": existing_comment.recipe_id,
                "message": existing_comment.message,
                "created_at": existing_comment.created_at,
                "updated_at": existing_comment.updated_at,
            }
            return jsonify(response_data)

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")


@blp.route("/recipes/uncomment/<int:recipe_in_search>/<int:comment_id_in_search>")
class UncommentFromRecipe(MethodView):
    @blp.response(201, CommentSchema)
    @jwt_required()
    def delete(self, recipe_in_search, comment_id_in_search):
        try:
            current_user_id = get_jwt_identity()["id"]
            recipe_id = recipe_in_search
            comment_exist = CommentModel.query.filter_by(
                id=comment_id_in_search
            ).first()

            if not comment_exist:
                return jsonify({"message": "The comment is not found"}), 404

            if comment_exist.user_id != current_user_id:
                jsonify({"message": "You are not allowed to delete this comment"}), 403

            if comment_exist.recipe_id != recipe_id:
                return jsonify({"message": "The comment is not found"}), 404

            comment_exist.delete_comment()

            return (
                jsonify({"message": "you have successfully deleted your comment"}),
                200,
            )

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
