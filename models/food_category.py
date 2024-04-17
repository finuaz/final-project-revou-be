from db import db
from flask_smorest import abort
import logging


class CategoryModel(db.Model):
    __tablename__ = "Category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    def __init__(self, category):
        self.category = category

    def add_category(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_category(cls, category_id):
        category = cls.query.filter_by(id=category_id).first()
        if category is None:
            logging.error(f"category with id {category_id} not found.")
            abort(404, f"category with id {category_id} not found.")
        return category

    def update_category(self, category_data):
        for key, value in category_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_category(self):
        db.session.delete(self)
        db.session.commit()
