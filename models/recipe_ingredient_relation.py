from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func
from flask import jsonify


class RecipeIngredientRelationModel(db.Model):
    __tablename__ = "Recipe_ingredient"

    recipe_id = db.Column(
        db.Integer, db.ForeignKey("Recipe.id"), primary_key=True, nullable=False
    )
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("Ingredient.id"), primary_key=True, nullable=False
    )
    amount = db.Column(db.String, nullable=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    recipes = db.relationship("RecipeModel", back_populates="recipe_ingredients")
    ingredients = db.relationship(
        "IngredientModel", back_populates="recipe_ingredients"
    )

    def __init__(self, recipe_id, ingredient_id, amount="adequate"):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.amount = amount

    def add_recipe_ingredient(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_recipe_ingredient(cls, recipe_ingredient_id):
        recipe_ingredient = cls.query.filter_by(id=recipe_ingredient_id).first()
        if recipe_ingredient is None:
            logging.error(
                f"recipe_ingredient with id {recipe_ingredient_id} not found."
            )
            return (
                jsonify(
                    {
                        "message",
                        "recipe ingredient with id {recipe_ingredient_id} not found.",
                    }
                ),
                404,
            )
        return recipe_ingredient

    def update_recipe_ingredient(self, recipe_ingredient_data):
        for key, value in recipe_ingredient_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_ingredient(self):
        db.session.delete(self)
        db.session.commit()
