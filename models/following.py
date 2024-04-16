from db import db
from flask_smorest import abort
import logging


class FollowingModel(db.Model):
    __tablename__ = "Following"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    followee_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), server_onupdate=db.func.now(), server_default=db.func.now()
    )

    def __init__(self, follower_id, followee_id):
        self.follower_id = follower_id
        self.followee_id = followee_id

    def add_following(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_following(cls, following_id):
        following = cls.query.filter_by(id=following_id).first()
        if following is None:
            logging.error(f"following with id {following_id} not found.")
            abort(404, f"following with id {following_id} not found.")
        return following

    def update_following(self, following_data):
        for key, value in following_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_following(self):
        db.session.delete(self)
        db.session.commit()
