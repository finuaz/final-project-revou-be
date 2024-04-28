from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, current_app

from werkzeug.exceptions import Forbidden

from models import RecipeModel, InstructionModel, RecipeInstructionRelationModel
from schemas import RecipeSchema, RecipeInstructionSchema

blp = Blueprint(
    "instructions", __name__, description="Operations on recipe instructions"
)


@blp.route("/<int:recipe_id>/instruction/create")
class AddInstruction(MethodView):
    @blp.arguments(RecipeInstructionSchema)
    @blp.response(201, RecipeInstructionSchema)
    @jwt_required()
    def post(self, recipe_id, instruction_data):
        current_user_id = get_jwt_identity()["id"]
        try:
            instruction = InstructionModel(
                author_id=current_user_id,
                order=instruction_data["order"],
                instruction=instruction_data["instruction"],
            )

            instruction.add_instruction()

        except IntegrityError:
            abort(400, message="instruction with that id already exists")
        except SQLAlchemyError as e:
            abort(
                500,
                message=f"An error occurred while creating the instruction: {str(e)}",
            )
        return instruction
