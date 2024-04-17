from db import db
from flask_smorest import abort
import logging


class RecipeIngredientRelationModel(db.Model):
    __tablename__ = "Recipe_ingredient"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    ingredient_id = db.Column(db.String, db.ForeignKey("Ingredient.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())

    recipes = db.relationship("RecipeModel", back_populates="recipe_ingredients")
    ingredients = db.relationship(
        "IngredientModel", back_populates="recipe_ingredients"
    )

    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id

    def add_recipe_ingredient(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_recipe_ingredient(cls, recipe_ingredient_id):
        recipe_ingredient = cls.query.filter_by(id=recipe_ingredient_id).first()
        if recipe_ingredient is None:
            logging.error(
                f"recipe_ingredient with id {recipe_ingredient_id} not found."
            )
            abort(404, f"recipe_ingredient with id {recipe_ingredient_id} not found.")
        return recipe_ingredient

    def update_recipe_ingredient(self, recipe_ingredient_data):
        for key, value in recipe_ingredient_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_ingredient(self):
        db.session.delete(self)
        db.session.commit()
