from sqlalchemy import Enum
from db import db
from flask_smorest import abort
import re
import logging


class RecipeOriginRelationModel(db.Model):
    __tablename__ = "Recipe_origin"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    origin_id = db.Column(db.String, db.ForeignKey("Origin.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
