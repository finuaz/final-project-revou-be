from db import db
from flask_smorest import abort
import logging


class RecipeOriginRelationModel(db.Model):
    __tablename__ = "Recipe_origin"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    origin_id = db.Column(db.String, db.ForeignKey("Origin.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())

    def __init__(self, recipe_id, origin_id):
        self.recipe_id = recipe_id
        self.origin_id = origin_id

    def add_recipe_origin(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_recipe_origin(cls, recipe_origin_id):
        recipe_origin = cls.query.filter_by(id=recipe_origin_id).first()
        if recipe_origin is None:
            logging.error(f"recipe_origin with id {recipe_origin_id} not found.")
            abort(404, f"recipe_origin with id {recipe_origin_id} not found.")
        return recipe_origin

    def update_recipe_origin(self, recipe_origin_data):
        for key, value in recipe_origin_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_origin(self):
        db.session.delete(self)
        db.session.commit()
