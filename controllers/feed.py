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

from models import RecipeModel
from schemas import RecipeSchema

from utils import (
    find_category,
    find_type,
    find_origin,
    find_tag,
    find_all_category,
    find_all_type,
    find_all_origin,
    find_all_tag,
)

blp = Blueprint("feeds", __name__, description="Operations on feeds")


@blp.route("/feeds/recipes/all")
class GetAllFeeds(MethodView):

    @blp.response(200, RecipeSchema(many=True))
    @cache.cached(timeout=180)
    def get(self):
        try:
            recipe = RecipeModel.query.all()
            if not recipe:
                abort(404, "No recipe created")

            # recipe.category = find_all_category(recipe.id)

            # recipe.type = find_all_type(recipe.id)

            # recipe.origin = find_all_origin(recipe.id)

            # recipe.tag = find_all_tag(recipe.id)

            serialized_recipe = RecipeSchema(many=True).dump(recipe)
            return jsonify(serialized_recipe), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")
