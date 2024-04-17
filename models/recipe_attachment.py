from db import db
from flask_smorest import abort
import logging


class AttachmentModel(db.Model):
    __tablename__ = "Attachment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipe.id"))
    attachment_link = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    recipes = db.relationship("RecipeModel", back_populates="attachments")

    def __init__(self, recipe_id, attachment_link):
        self.recipe_id = recipe_id
        self.attachment_link = attachment_link

    def add_attachment(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_attachment(cls, attachment_id):
        attachment = cls.query.filter_by(id=attachment_id).first()
        if attachment is None:
            logging.error(f"attachment with id {attachment_id} not found.")
            abort(404, f"attachment with id {attachment_id} not found.")
        return attachment

    def update_attachment(self, attachment_data):
        for key, value in attachment_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_attachment(self):
        db.session.delete(self)
        db.session.commit()
