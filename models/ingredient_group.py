from db import db
from flask_smorest import abort
import logging


class IngredientGroupRelationModel(db.Model):
    __tablename__ = "Ingredient_group"

    ingredient_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    group_id = db.Column(db.String, db.ForeignKey("Group.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())

    def __init__(self, ingredient_id, group_id):
        self.ingredient_id = ingredient_id
        self.group_id = group_id

    def add_ingredient_group(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_ingredient_group(cls, ingredient_group_id):
        ingredient_group = cls.query.filter_by(id=ingredient_group_id).first()
        if ingredient_group is None:
            logging.error(f"ingredient_group with id {ingredient_group_id} not found.")
            abort(404, f"ingredient_group with id {ingredient_group_id} not found.")
        return ingredient_group

    def update_ingredient_group(self, ingredient_group_data):
        for key, value in ingredient_group_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_ingredient_group(self):
        db.session.delete(self)
        db.session.commit()
