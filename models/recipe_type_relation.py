from sqlalchemy import Enum
from db import db
from flask_smorest import abort
import re
import logging


class RecipeTypeRelationModel(db.Model):
    __tablename__ = "Recipe_type"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    type_id = db.Column(db.String, db.ForeignKey("Type.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
