from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, current_app
from db import db

from werkzeug.exceptions import Forbidden

from models import RecipeModel, InstructionModel
from schemas import RecipeSchema, RecipeInstructionSchema

blp = Blueprint(
    "instructions", __name__, description="Operations on recipe instructions"
)


@blp.route("/instructions/create/<int:related_recipe_id>")
class AddInstruction(MethodView):

    @blp.arguments(RecipeInstructionSchema)
    @blp.response(201, RecipeInstructionSchema)
    @jwt_required()
    def post(self, instruction_data, related_recipe_id):
        current_user_id = get_jwt_identity()["id"]

        try:
            recipe = RecipeModel.get_recipe(related_recipe_id)
            if not recipe:
                abort(404, message=f"Recipe with id {related_recipe_id} not found.")

            instruction = InstructionModel(
                author_id=current_user_id,
                recipe_id=related_recipe_id,
                order=instruction_data["order"],
                instruction=instruction_data["instruction"],
            )

            instruction.add_instruction()

        except IntegrityError:
            abort(400, message="instruction with that order already exists")
        except SQLAlchemyError as e:
            abort(
                500,
                message=f"An error occurred while creating the instruction: {str(e)}",
            )
        return instruction


@blp.route("/instructions/<int:related_recipe_id>")
class GetAllInstruction(MethodView):

    @blp.response(200, RecipeInstructionSchema(many=True))
    def get(self, related_recipe_id):

        try:
            instructions = (
                InstructionModel.query.filter_by(recipe_id=related_recipe_id)
                .order_by(asc(InstructionModel.order))
                .all()
            )

            if not instructions:
                abort(404, "Instructions not found")

            serialized_instruction = RecipeInstructionSchema(many=True).dump(
                instructions
            )

            return jsonify(serialized_instruction), 200

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            abort(500, "Internal Server Error")
        except Exception as e:
            current_app.logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, "Internal Server Error")


@blp.route("/instructions/edit/<int:related_recipe_id>/<int:order_number>")
class EditInstruction(MethodView):

    @blp.arguments(RecipeInstructionSchema)
    @blp.response(201, RecipeInstructionSchema)
    @jwt_required()
    def put(self, instruction_data, related_recipe_id, order_number):
        user_id = get_jwt_identity()["id"]
        instruction = (
            InstructionModel.query.filter_by(recipe_id=related_recipe_id)
            .filter_by(order=order_number)
            .first()
        )

        if not instruction:
            abort(404, "Instruction not found")

        if instruction.author_id != user_id:
            abort(403, "You are not authorized to edit this recipe")

        try:
            new_order = instruction_data.get("order")
            existing_instruction = InstructionModel.query.filter_by(
                recipe_id=related_recipe_id, order=new_order
            ).first()
            if existing_instruction and existing_instruction != instruction:

                return (
                    jsonify(
                        {
                            "message": "Another instruction with the same order already exists"
                        }
                    ),
                    400,
                )

            instruction.order = new_order
            instruction.update_instruction(instruction_data)

            return RecipeInstructionSchema().dump(instruction), 200

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to update recipe information: {str(e)}")


@blp.route("/instructions/delete/<int:related_recipe_id>/<int:order_number>")
class DeleteInstruction(MethodView):

    @blp.response(201, RecipeInstructionSchema)
    @jwt_required()
    def delete(self, related_recipe_id, order_number):
        user_id = get_jwt_identity()["id"]
        instruction = (
            InstructionModel.query.filter_by(recipe_id=related_recipe_id)
            .filter_by(order=order_number)
            .first()
        )

        if not instruction:
            abort(404, "Instruction not found")

        if instruction.author_id != user_id:
            abort(403, "You are not authorized to edit this recipe")

        try:
            instruction.delete_instruction()
            print("-- Instruction deleted successfully --")
            return "", 204

        except Forbidden as e:
            abort(403, description=str(e))

        except Exception as e:
            abort(500, description=f"Failed to delete recipe information: {str(e)}")
