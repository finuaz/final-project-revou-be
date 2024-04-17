from db import db
from flask_smorest import abort
import logging


class RecipeTagRelationModel(db.Model):
    __tablename__ = "Recipe_tag"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    tag_id = db.Column(db.String, db.ForeignKey("Tag.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())

    recipes = db.relationship("RecipeModel", back_populates="recipe_tags")
    tags = db.relationship("TagModel", back_populates="recipe_tags")

    def __init__(self, recipe_id, tag_id):
        self.recipe_id = recipe_id
        self.tag_id = tag_id

    def add_recipe_tag(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_recipe_tag(cls, recipe_tag_id):
        recipe_tag = cls.query.filter_by(id=recipe_tag_id).first()
        if recipe_tag is None:
            logging.error(f"recipe_tag with id {recipe_tag_id} not found.")
            abort(404, f"recipe_tag with id {recipe_tag_id} not found.")
        return recipe_tag

    def update_recipe_tag(self, recipe_tag_data):
        for key, value in recipe_tag_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_tag(self):
        db.session.delete(self)
        db.session.commit()
