from db import db
from flask_smorest import abort
import logging


class LikeModel(db.Model):
    __tablename__ = "Like"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"))
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    users = db.relationship("UserModel", back_populates="likes")
    recipes = db.relationship("RecipeModel", back_populates="likes")

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id

    def add_like(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_like(cls, like_id):
        like = cls.query.filter_by(id=like_id).first()
        if like is None:
            logging.error(f"like with id {like_id} not found.")
            abort(404, f"like with id {like_id} not found.")
        return like

    def update_like(self, like_data):
        for key, value in like_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_like(self):
        db.session.delete(self)
        db.session.commit()
