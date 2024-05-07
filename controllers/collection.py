import logging

from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, current_app

from models import (
    RecipeModel,
    UserModel,
    LikeModel,
    FollowingModel,
    UserRole,
)
from schemas import RecipePlusPlusSchema
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
                return jsonify({"message", "You have not created any recipe"}), 404

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
                return jsonify({"message", "the user have not created any recipe"}), 404

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


@blp.route("/collection/recipes/creator/<string:author_name_in_search>")
class GetAllRecipesCreatedByUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    # @jwt_required()
    def get(self, author_name_in_search):
        user = UserModel.query.filter_by(first_name=author_name_in_search).first()

        if not user:
            user = UserModel.query.filter_by(last_name=author_name_in_search).first()

            if not user:
                user = UserModel.query.filter_by(username=author_name_in_search).first()

                if not user:
                    return jsonify({"message": "the user is not found"}), 404

        try:
            recipes = RecipeModel.query.filter_by(author_id=user.id).all()

            if not recipes:
                return jsonify({"message", "The user has not created any recipe"}), 404

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


@blp.route("/collection/recipes/liked")
class GetAllLikedRecipes(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        recipes = []

        try:
            liked_recipes = LikeModel.query.filter_by(user_id=current_user_id).all()

            for liked_recipe in liked_recipes:

                recipe = RecipeModel.query.filter_by(id=liked_recipe.recipe_id).first()

                if recipe:

                    recipe.categories = find_all_category(liked_recipe.recipe_id)
                    recipe.type = find_all_type(liked_recipe.recipe_id)
                    recipe.origin = find_all_origin(liked_recipe.recipe_id)
                    recipe.tags = find_all_tag(liked_recipe.recipe_id)
                    recipe.like_count = get_likes(liked_recipe.recipe_id)
                    recipe.rating = get_rating(liked_recipe.recipe_id)
                    recipe.attachment = find_attachment(liked_recipe.recipe_id)
                    recipe.is_chef_recipe = chef_recipe_check(liked_recipe.recipe_id)

                    recipes.append(recipe)

            serialized_recipes = RecipePlusPlusSchema(many=True).dump(recipes)
            return jsonify(serialized_recipes), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/collection/recipes/followed")
class GetAllRecipesFromFollowedUser(MethodView):

    @blp.response(200, RecipePlusPlusSchema(many=True))
    # @cache.cached(timeout=60 / 2)
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()["id"]

        recipes = []

        try:
            followed_users = FollowingModel.query.filter_by(
                follower_id=current_user_id
            ).all()

            if not followed_users:
                return jsonify({"message", "You are not following any user"}), 404

            for followed_user in followed_users:

                user_recipes = RecipeModel.query.filter_by(
                    author_id=followed_user.followed_id
                ).all()

                if not user_recipes:
                    continue

                for recipe in user_recipes:

                    if recipe:

                        recipe.categories = find_all_category(recipe.id)
                        recipe.type = find_all_type(recipe.id)
                        recipe.origin = find_all_origin(recipe.id)
                        recipe.tags = find_all_tag(recipe.id)
                        recipe.like_count = get_likes(recipe.id)
                        recipe.rating = get_rating(recipe.id)
                        recipe.attachment = find_attachment(recipe.id)
                        recipe.is_chef_recipe = chef_recipe_check(recipe.id)

                        recipes.append(recipe)

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
        try:
            chefs = UserModel.query.filter_by(role=UserRole.CHEF).all()

            if not chefs:
                return jsonify({"message", "there is no chef here"}), 404

            for chef in chefs:
                recipes = RecipeModel.query.filter_by(author_id=chef.id).all()

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

            return jsonify({"message": "OK"}), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")
