import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, request

from models import RecipeModel, CommentModel
from schemas import CommentSchema
from utils import get_comments

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

            recipe = RecipeModel.query.filter_by(id=recipe_in_search).first()

            if not recipe:
                abort(404, message="Recipe is not found")

            if not comment_message:
                abort(403, message="Comment message is required")

            comment = CommentModel(
                recipe_id=recipe_in_search,
                user_id=current_user_id,
                message=comment_message,
            )

            comment.add_comment()

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
                abort(404, message="Recipe is not found")

            if existing_comment.user_id != current_user_id:
                abort(403, message="you are not authorized to edit this comment")

            if not comment_message:
                abort(403, message="Comment message is required")

            if not existing_comment:
                abort(404, message="The comment is not found")

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
                abort(404, message="The comment is not found")

            if comment_exist.user_id != current_user_id:
                abort(404, message="You are not allowed to delete this comment")

            if comment_exist.recipe_id != recipe_id:
                abort(404, message="The comment is not found")

            comment_exist.delete_comment()

            return (
                jsonify({"message": "you have successfully deleted your comment"}),
                200,
            )

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
