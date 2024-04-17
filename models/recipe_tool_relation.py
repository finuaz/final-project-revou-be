from db import db
from flask_smorest import abort
import logging


class RecipeToolRelationModel(db.Model):
    __tablename__ = "Recipe_tool"

    recipe_id = db.Column(db.String, db.ForeignKey("Recipe.id"), nullable=False)
    tool_id = db.Column(db.String, db.ForeignKey("Tool.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())

    def __init__(self, recipe_id, tool_id):
        self.recipe_id = recipe_id
        self.tool_id = tool_id

    def add_recipe_tool(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_recipe_tool(cls, recipe_tool_id):
        recipe_tool = cls.query.filter_by(id=recipe_tool_id).first()
        if recipe_tool is None:
            logging.error(f"recipe_tool with id {recipe_tool_id} not found.")
            abort(404, f"recipe_tool with id {recipe_tool_id} not found.")
        return recipe_tool

    def update_recipe_tool(self, recipe_tool_data):
        for key, value in recipe_tool_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe_tool(self):
        db.session.delete(self)
        db.session.commit()
