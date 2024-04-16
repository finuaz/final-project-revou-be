from sqlalchemy import Enum
from db import db
from flask_smorest import abort
import re
import logging


class RecipeToolRelationModel(db.Model):
    __tablename__ = "Recipe_tool"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    tool_id = db.Column(db.String, db.ForeignKey("Tool.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
