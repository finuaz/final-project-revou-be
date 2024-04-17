from db import db
from flask_smorest import abort
import logging


class RecipeTypeRelationModel(db.Model):
    __tablename__ = "Recipe_type"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    type_id = db.Column(db.String, db.ForeignKey("Type.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())

    def __init__(self, recipe_id, type_id):
        self.recipe_id = recipe_id
        self.type_id = type_id

    def add_recipe_type(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_recipe_type(cls, recipe_type_id):
        recipe_type = cls.query.filter_by(id=recipe_type_id).first()
        if recipe_type is None:
            logging.error(f"recipe_type with id {recipe_type_id} not found.")
            abort(404, f"recipe_type with id {recipe_type_id} not found.")
        return recipe_type

    def update_recipe_type(self, recipe_type_data):
        for key, value in recipe_type_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_type(self):
        db.session.delete(self)
        db.session.commit()
