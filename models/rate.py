from db import db
from flask_smorest import abort
import logging


class RateModel(db.Model):
    __tablename__ = "Rate"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"))
    value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    user = db.relationship("UserModel", back_populates="likes")
    recipe = db.relationship("RecipeModel", back_populates="likes")

    def __init__(self, user_id, recipe_id, value):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.value = value

    def add_rate(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_rate(cls, rate_id):
        rate = cls.query.filter_by(id=rate_id).first()
        if rate is None:
            logging.error(f"rate with id {rate_id} not found.")
            abort(404, f"rate with id {rate_id} not found.")
        return rate

    def update_rate(self, rate_data):
        for key, value in rate_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_rate(self):
        db.session.delete(self)
        db.session.commit()
