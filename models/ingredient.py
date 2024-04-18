from db import db
from flask_smorest import abort
import logging


class IngredientModel(db.Model):
    __tablename__ = "Ingredient"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient = db.Column(db.String(40), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    calories_per_unit = db.Column(db.DECIMAL(10, 2), nullable=True)
    fat_per_unit = db.Column(db.DECIMAL(10, 2), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_onupdate=db.func.now(), server_default=db.func.now()
    )

    recipe_ingredients = db.relationship(
        "RecipeIngredientRelationModel", back_populates="ingredients"
    )
    ingredient_groups = db.relationship(
        "IngredientGroupRelationModel", back_populates="ingredients"
    )

    def __init__(self, ingredient, unit, calories_per_unit, fat_per_unit):
        self.ingredient = ingredient
        self.unit = unit
        self.calories_per_unit = calories_per_unit
        self.fat_per_unit = fat_per_unit

    def add_ingredient(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_ingredient(cls, ingredient_id):
        ingredient = cls.query.filter_by(id=ingredient_id).first()
        if ingredient is None:
            logging.error(f"ingredient with id {ingredient_id} not found.")
            abort(404, f"ingredient with id {ingredient_id} not found.")
        return ingredient

    def update_ingredient(self, ingredient_data):
        for key, value in ingredient_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_ingredient(self):
        db.session.delete(self)
        db.session.commit()
