from db import db
from flask_smorest import abort
import logging


class CommentModel(db.Model):
    __tablename__ = "Comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    users = db.relationship("UserModel", back_populates="comments")
    recipes = db.relationship("RecipeModel", back_populates="comments")

    def __init__(self, recipe_id, user_id, message):
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.message = message

    def add_comment(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_comment(cls, comment_id):
        comment = cls.query.filter_by(id=comment_id).first()
        if comment is None:
            logging.error(f"comment with id {comment_id} not found.")
            abort(404, f"comment with id {comment_id} not found.")
        return comment

    def update_comment(self, comment_data):
        for key, value in comment_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
