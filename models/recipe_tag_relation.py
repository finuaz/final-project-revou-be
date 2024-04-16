from sqlalchemy import Enum
from db import db
from flask_smorest import abort
import re
import logging


class RecipeTagRelationModel(db.Model):
    __tablename__ = "Recipe_tag"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    tag_id = db.Column(db.String, db.ForeignKey("Tag.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
