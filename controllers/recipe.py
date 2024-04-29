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

from models import (
    RecipeModel,
    CategoryModel,
    RecipeCategoryRelationModel,
    TypeModel,
    RecipeTypeRelationModel,
    OriginModel,
    RecipeOriginRelationModel,
    TagModel,
    RecipeTagRelationModel,
)
from schemas import (
    RecipeSchema,
)

blp = Blueprint("recipes", __name__, description="Operations on recipes")


@blp.route("/recipes/create")
class RecipeRegister(MethodView):
    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeSchema)
    @jwt_required()
    def post(self, recipe_data):
        current_user_id = get_jwt_identity()["id"]
        try:
            recipe = RecipeModel(
                author_id=current_user_id,
                title=recipe_data["title"],
                description=recipe_data["description"],
                nutriscore=recipe_data["nutriscore"],
                cooktime=recipe_data["cooktime"],
                complexity=recipe_data["complexity"],
                servings=recipe_data["servings"],
                budget=recipe_data["budget"],
                instruction=recipe_data["instruction"],
            )

            recipe.add_recipe()

            # add category
            if "category" in recipe_data:
                category = CategoryModel.query.filter_by(
                    category=recipe_data["category"]
                ).first()

                if not category:
                    category = CategoryModel(category=recipe_data["category"])
                    category.add_category()

                recipe_category = RecipeCategoryRelationModel(
                    recipe_id=recipe.id,
                    category_id=category.id,
                )

                recipe_category.add_recipe_category()
                recipe.category = category.category

            # add type
            if "type" in recipe_data:
                type = TypeModel.query.filter_by(type=recipe_data["type"]).first()

                if not type:
                    type = TypeModel(type=recipe_data["type"])
                    type.add_type()

                recipe_type = RecipeTypeRelationModel(
                    recipe_id=recipe.id,
                    type_id=type.id,
                )

                recipe_type.add_recipe_type()
                recipe.type = type.type

            # add origin
            if "origin" in recipe_data:
                origin = OriginModel.query.filter_by(
                    origin=recipe_data["origin"]
                ).first()

                if not origin:
                    origin = OriginModel(origin=recipe_data["origin"])
                    origin.add_origin()

                recipe_origin = RecipeOriginRelationModel(
                    recipe_id=recipe.id,
                    origin_id=origin.id,
                )

                recipe_origin.add_recipe_origin()
                recipe.origin = origin.origin

            # add tag
            if "tag" in recipe_data:
                tags = recipe_data["tag"]

                for tag_name in tags:
                    tag = TagModel.query.filter_by(tagname=tag_name).first()

                    if not tag:
                        tag = TagModel(tagname=tag_name)
                        tag.add_tag()

                    recipe_tag = RecipeTagRelationModel(
                        recipe_id=recipe.id,
                        tag_id=tag.id,
                    )

                    recipe_tag.add_recipe_tag()
                recipe.tag = tags

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
        return recipe


@blp.route("/recipes/details/<int:recipe_in_details_by_id>")
class RecipeDetailsById(MethodView):
    @blp.response(201, RecipeSchema)
    @cache.cached(timeout=60)
    def get(self, recipe_in_details_by_id):
        try:
            recipe = RecipeModel.query.filter_by(id=recipe_in_details_by_id).first()
            if not recipe:
                abort(404, "Recipe not found")

            # finding category
            recipe_category = RecipeCategoryRelationModel.query.filter_by(
                recipe_id=recipe_in_details_by_id
            ).first()
            category = CategoryModel.query.filter_by(
                id=recipe_category.category_id
            ).first()
            recipe.category = category.category

            # finding type
            recipe_type = RecipeTypeRelationModel.query.filter_by(
                recipe_id=recipe_in_details_by_id
            ).first()
            type = TypeModel.query.filter_by(id=recipe_type.type_id).first()
            recipe.type = type.type

            # finding origin
            recipe_origin = RecipeOriginRelationModel.query.filter_by(
                recipe_id=recipe_in_details_by_id
            ).first()
            origin = OriginModel.query.filter_by(id=recipe_origin.origin_id).first()
            recipe.origin = origin.origin

            # finding tag
            recipe_tags = RecipeTagRelationModel.query.filter_by(
                recipe_id=recipe_in_details_by_id
            ).all()
            tags = [
                TagModel.query.get(recipe_tag.tag_id).tagname
                for recipe_tag in recipe_tags
            ]
            recipe.tag = tags

            serialized_recipe = RecipeSchema().dump(recipe)
            return jsonify(serialized_recipe), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/recipes/details/<string:recipe_in_details_by_title>")
class RecipeDetailsByTitle(MethodView):

    @blp.response(201, RecipeSchema)
    @cache.cached(timeout=60)
    def get(self, recipe_in_details_by_title):
        try:
            recipe = RecipeModel.query.filter_by(
                title=recipe_in_details_by_title
            ).first()
            if not recipe:
                abort(404, "Recipe not found")

            serialized_recipe = RecipeSchema().dump(recipe)
            return jsonify(serialized_recipe), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/recipes/edit/<int:recipe_in_details_by_id>")
class RecipeUpdate(MethodView):
    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeSchema)
    @jwt_required()
    def put(self, recipe_data, recipe_in_details_by_id):

        user_id = get_jwt_identity()["id"]
        recipe = RecipeModel.query.filter_by(id=recipe_in_details_by_id).first()

        if recipe.author_id != user_id:
            abort(403, "You are not authorized to edit this recipe")

        try:

            recipe.update_recipe(recipe_data)

            return RecipeSchema().dump(recipe), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/recipes/delete/<int:recipe_in_details_by_id>")
class RecipeDelete(MethodView):

    @blp.response(204, "Recipe deleted successfully")
    @jwt_required()
    def delete(self, recipe_in_details_by_id):
        print("ok")
        user_id = get_jwt_identity()["id"]
        recipe = RecipeModel.query.filter_by(id=recipe_in_details_by_id).first()
        print("step 1")

        if not recipe:
            abort(404, "Recipe not found")
        print("step 1.2")
        if recipe.author_id != user_id:
            abort(403, "You are not authorized to delete this recipe")
        print("step 2")

        try:
            recipe.delete_recipe()

            return jsonify({"message": "Recipe deleted successfully"}), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to delete recipe: {str(e)}")
