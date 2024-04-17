from db import db
from flask_smorest import abort
import logging


class GroupModel(db.Model):
    __tablename__ = "Group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group = db.Column(db.String(25), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    ingredient_groups = db.relationship(
        "IngredientGroupRelationModel", back_populates="groups"
    )

    def __init__(self, group):
        self.group = group

    def add_group(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_group(cls, group_id):
        group = cls.query.filter_by(id=group_id).first()
        if group is None:
            logging.error(f"group with id {group_id} not found.")
            abort(404, f"group with id {group_id} not found.")
        return group

    def update_group(self, group_data):
        for key, value in group_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_group(self):
        db.session.delete(self)
        db.session.commit()