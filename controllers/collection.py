import logging
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

from models import (
    RecipeModel,
    UserModel,
    RecipeCategoryRelationModel,
    CategoryModel,
    RecipeTypeRelationModel,
    TypeModel,
    RecipeOriginRelationModel,
    OriginModel,
    RecipeTagRelationModel,
    TagModel,
)
from schemas import RecipeSchema, RecipePlusPlusSchema

from utils import (
    find_all_category,
    find_all_type,
    find_all_origin,
    find_all_tag,
    get_likes,
    get_rating,
    find_attachment,
    chef_recipe_check,
)

logging.basicConfig(level=logging.INFO)

blp = Blueprint("collections", __name__, description="Operations on collections")


@blp.route("/collection/recipes/self-created")
class GetAllSelfCreatedRecipes(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        try:
            recipes = RecipeModel.query.filter_by(author_id=current_user_id).all()

            if not recipes:
                abort(404, "You have not created any recipe")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/creator/<int:author_id>")
class GetAllRecipesCreatedByUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    # @jwt_required()
    def get(self, author_id):

        try:
            recipes = RecipeModel.query.filter_by(author_id=author_id).all()

            if not recipes:
                abort(404, "You have not created any recipe")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/creator/<string:author_name>")
class GetAllRecipesCreatedByUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    # @jwt_required()
    def get(self, author_name):
        user = UserModel.query.filter(first_name=author_name).first()

        if not user:
            user = UserModel.query.filter_by(last_name=author_name).first()

            if not user:
                user = UserModel.query.filter_by(username=author_name).first()

                if not user:
                    return jsonify({"message": "the user is not found"}), 404

        try:
            recipes = RecipeModel.query.filter_by(author_id=user.id).all()

            if not recipes:
                abort(404, "You have not created any recipe")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)
                recipe.like_count = get_likes(recipe.id)
                recipe.rating = get_rating(recipe.id)
                recipe.attachment = find_attachment(recipe.id)
                recipe.is_chef_recipe = chef_recipe_check(recipe.id)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/creator/chef")
class GetAllRecipesCreatedByChef(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        return


@blp.route("/collection/recipes/liked")
class GetAllLikedRecipes(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        return


@blp.route("/collection/recipes/followed")
class GetAllRecipesFromFollowedUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        return
