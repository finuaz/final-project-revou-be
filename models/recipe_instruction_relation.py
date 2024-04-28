from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func


class RecipeInstructionRelationModel(db.Model):
    __tablename__ = "Recipe_instruction"

    recipe_id = db.Column(
        db.Integer, db.ForeignKey("Recipe.id"), primary_key=True, nullable=False
    )
    instruction_id = db.Column(
        db.Integer, db.ForeignKey("Instruction.id"), primary_key=True, nullable=False
    )
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    recipes = db.relationship("RecipeModel", back_populates="recipe_instructions")
    instructions = db.relationship(
        "InstructionModel", back_populates="recipe_instructions"
    )

    def __init__(self, recipe_id, instruction_id):
        self.recipe_id = recipe_id
        self.instruction_id = instruction_id

    def add_recipe_instruction(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_recipe_instruction(cls, recipe_instruction_id):
        recipe_instruction = cls.query.filter_by(id=recipe_instruction_id).first()
        if recipe_instruction is None:
            logging.error(
                f"recipe_instruction with id {recipe_instruction_id} not found."
            )
            abort(404, f"recipe_instruction with id {recipe_instruction_id} not found.")
        return recipe_instruction

    def update_recipe_instruction(self, recipe_instruction_data):
        for key, value in recipe_instruction_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_instruction(self):
        db.session.delete(self)
        db.session.commit()
