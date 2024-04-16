from sqlalchemy import Enum
from db import db
from flask_smorest import abort
import re
import logging


class RecipeIngredientRelationModel(db.Model):
    __tablename__ = "Recipe_ingredient"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    ingredient_id = db.Column(db.String, db.ForeignKey("Ingredient.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
