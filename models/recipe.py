from db import db
from flask_smorest import abort
import logging
from sqlalchemy import func


class RecipeModel(db.Model):
    __tablename__ = "Recipe"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    cooktime = db.Column(db.String(20), nullable=False)
    complexity = db.Column(db.String(20), nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.DECIMAL(10, 2), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    likes = db.relationship("LikeModel", back_populates="recipes")
    comments = db.relationship("CommentModel", back_populates="recipes")
    rates = db.relationship("RateModel", back_populates="recipes")
    attachments = db.relationship("AttachmentModel", back_populates="recipes")
    nutritions = db.relationship("NutritionModel", back_populates="recipes")

    recipe_categories = db.relationship(
        "RecipeCategoryRelationModel", back_populates="recipes"
    )
    recipe_ingredients = db.relationship(
        "RecipeIngredientRelationModel", back_populates="recipes"
    )
    recipe_origins = db.relationship(
        "RecipeOriginRelationModel", back_populates="recipes"
    )
    recipe_tags = db.relationship("RecipeTagRelationModel", back_populates="recipes")
    recipe_tools = db.relationship("RecipeToolRelationModel", back_populates="recipes")
    recipe_types = db.relationship("RecipeTypeRelationModel", back_populates="recipes")

    def __init__(
        self,
        author_id,
        title,
        description,
        cooktime,
        complexity,
        servings,
        budget,
        instructions,
        view_count,
    ):
        self.author_id = author_id
        self.title = title
        self.description = description
        self.cooktime = cooktime
        self.complexity = complexity
        self.servings = servings
        self.budget = budget
        self.instructions = instructions
        self.view_count = view_count

    def add_recipe(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_recipe(cls, recipe_id):
        recipe = cls.query.filter_by(id=recipe_id).first()
        if recipe is None:
            logging.error(f"recipe with id {recipe_id} not found.")
            abort(404, f"recipe with id {recipe_id} not found.")
        return recipe

    def update_recipe(self, recipe_data):
        for key, value in recipe_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_recipe(self):
        db.session.delete(self)
        db.session.commit()
