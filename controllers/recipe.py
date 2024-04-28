from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, current_app

from werkzeug.exceptions import Forbidden

from models import RecipeModel
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
                instructions=recipe_data["instructions"],
            )

            recipe.add_recipe()

        except IntegrityError:
            abort(400, message="recipe with that title already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the recipe: {str(e)}")
        return recipe


@blp.route("/recipes/details/<int:recipe_in_details_by_id>")
class RecipeDetailsById(MethodView):
    @blp.response(201, RecipeSchema)
    def get(self, recipe_in_details_by_id):
        try:
            recipe = RecipeModel.query.filter_by(id=recipe_in_details_by_id).first()
            if not recipe:
                abort(404, "Recipe not found")

            serialized_user = RecipeSchema().dump(recipe)
            return jsonify(serialized_user), 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/recipes/details/<string:recipe_in_details_by_title>")
class RecipeDetailsByTitle(MethodView):
    @blp.response(201, RecipeSchema)
    def get(self, recipe_in_details_by_title):
        try:
            recipe = RecipeModel.query.filter_by(
                title=recipe_in_details_by_title
            ).first()
            if not recipe:
                abort(404, "Recipe not found")

            serialized_user = RecipeSchema().dump(recipe)
            return jsonify(serialized_user), 200
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
