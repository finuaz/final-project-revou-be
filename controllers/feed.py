from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, current_app
from passlib.hash import pbkdf2_sha512
from extensions import cache

from werkzeug.exceptions import Forbidden

from models import (
    RecipeModel,
    RecipeCategoryRelationModel,
    CategoryModel,
    RecipeTypeRelationModel,
    TypeModel,
    RecipeOriginRelationModel,
    OriginModel,
    RecipeTagRelationModel,
    TagModel,
)
from schemas import RecipeSchema

from utils import (
    find_all_category,
    find_all_type,
    find_all_origin,
    find_all_tag,
)

blp = Blueprint("feeds", __name__, description="Operations on feeds")


@blp.route("/feeds/recipes/all")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipeSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self):
        try:
            recipes = RecipeModel.query.all()
            if not recipes:
                abort(404, "No recipe created")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)

            serialized_recipes = RecipeSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/category/<string:recipe_category_in_search>")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipeSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_category_in_search):
        try:
            category = CategoryModel.query.filter_by(
                category=recipe_category_in_search
            ).first()

            recipe_categories = RecipeCategoryRelationModel.query.filter_by(
                category_id=category.id
            ).all()

            recipes = []

            for recipe_category in recipe_categories:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_category.recipe_id).all()
                )

            if not recipes:
                abort(404, "No recipe created under the category name")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)

            serialized_recipes = RecipeSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/type/<string:recipe_type_in_search>")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipeSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_type_in_search):
        try:
            type = TypeModel.query.filter_by(type=recipe_type_in_search).first()

            recipe_types = RecipeTypeRelationModel.query.filter_by(
                type_id=type.id
            ).all()

            recipes = []

            for recipe_type in recipe_types:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_type.recipe_id).all()
                )

            if not recipes:
                abort(404, "No recipe created under the type name")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)

            serialized_recipes = RecipeSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/origin/<string:recipe_origin_in_search>")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipeSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_origin_in_search):
        try:
            origin = OriginModel.query.filter_by(origin=recipe_origin_in_search).first()

            recipe_origins = RecipeOriginRelationModel.query.filter_by(
                origin_id=origin.id
            ).all()

            recipes = []

            for recipe_origin in recipe_origins:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_origin.recipe_id).all()
                )

            if not recipes:
                abort(404, "No recipe created under the origin name")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)

            serialized_recipes = RecipeSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/feeds/recipes/filter-by/tag/<string:recipe_tag_in_search>")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipeSchema(many=True))
    # @cache.cached(timeout=60 * 3)
    def get(self, recipe_tag_in_search):
        try:
            tag = TagModel.query.filter_by(tagname=recipe_tag_in_search).first()

            recipe_tags = RecipeTagRelationModel.query.filter_by(tag_id=tag.id).all()

            recipes = []

            for recipe_tag in recipe_tags:
                recipes.extend(
                    RecipeModel.query.filter_by(id=recipe_tag.recipe_id).all()
                )

            if not recipes:
                abort(404, "No recipe created under the tag name")

            for recipe in recipes:
                recipe.categories = find_all_category(recipe.id)
                recipe.type = find_all_type(recipe.id)
                recipe.origin = find_all_origin(recipe.id)
                recipe.tags = find_all_tag(recipe.id)

            serialized_recipes = RecipeSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")
