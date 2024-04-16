from sqlalchemy import Enum
from db import db
from flask_smorest import abort
import re
import logging


class RecipeCategoryRelationModel(db.Model):
    __tablename__ = "Recipe_category"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    category_id = db.Column(db.String, db.ForeignKey("Category.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
