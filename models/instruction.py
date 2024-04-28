from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func


class InstructionModel(db.Model):
    __tablename__ = "Instruction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    order = db.Column(db.Integer, nullable=False, unique=True)
    instruction = db.Column(db.String(120), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    recipe_instructions = db.relationship(
        "RecipeInstructionRelationModel", back_populates="instructions"
    )

    def __init__(self, author_id, order, instruction):
        self.author_id = author_id
        self.order = order
        self.instruction = instruction

    def add_instruction(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            logging.error(f"Failed to add instruction: {str(e)}")
            db.session.rollback()
            raise

    @classmethod
    def get_instruction(cls, instruction_id):
        instruction = cls.query.filter_by(id=instruction_id).first()
        if instruction is None:
            logging.error(f"instruction with id {instruction_id} not found.")
            abort(404, f"instruction with id {instruction_id} not found.")
        return instruction

    def update_instruction(self, instruction_data):
        for key, value in instruction_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_instruction(self):
        db.session.delete(self)
        db.session.commit()
