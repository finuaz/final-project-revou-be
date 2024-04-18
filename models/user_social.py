from db import db
from flask_smorest import abort
import logging
from datetime import datetime


class SocialModel(db.Model):
    __tablename__ = "Socials"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    phone = db.Column(db.String, nullable=True)
    facebook = db.Column(db.String, nullable=True)
    instagram = db.Column(db.String, nullable=True)
    twitter = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_onupdate=db.func.now(), server_default=db.func.now()
    )

    users = db.relationship("UserModel", back_populates="socials")

    def __init__(self, user_id, phone, facebook, instagram, twitter):
        self.user_id = user_id
        self.phone = phone
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter

    def add_user_social(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_user_social(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        if user is None:
            logging.error(f"User social with id {user_id} not found.")
            abort(404, f"User social with id {user_id} not found.")
        return user

    def update_user_social(self, platform):
        for key, value in platform.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_user_social(self):
        db.session.delete(self)
        db.session.commit()
