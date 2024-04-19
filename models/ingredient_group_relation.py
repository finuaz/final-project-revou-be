from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func


class IngredientGroupRelationModel(db.Model):
    __tablename__ = "Ingredient_group"

    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("Ingredient.id"), primary_key=True, nullable=False
    )
    group_id = db.Column(
        db.Integer, db.ForeignKey("Group.id"), primary_key=True, nullable=False
    )
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    ingredients = db.relationship("IngredientModel", back_populates="ingredient_groups")
    groups = db.relationship("GroupModel", back_populates="ingredient_groups")

    def __init__(self, ingredient_id, group_id):
        self.ingredient_id = ingredient_id
        self.group_id = group_id

    def add_ingredient_group(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_ingredient_group(cls, ingredient_group_id):
        ingredient_group = cls.query.filter_by(id=ingredient_group_id).first()
        if ingredient_group is None:
            logging.error(f"ingredient_group with id {ingredient_group_id} not found.")
            abort(404, f"ingredient_group with id {ingredient_group_id} not found.")
        return ingredient_group

    def update_ingredient_group(self, ingredient_group_data):
        for key, value in ingredient_group_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_ingredient_group(self):
        db.session.delete(self)
        db.session.commit()
