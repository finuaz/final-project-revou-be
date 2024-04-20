from db import db
from flask_smorest import abort
import re
import logging
from enum import Enum
from sqlalchemy import func


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"
    CHEF = "chef"
    EXPERT = "expert"


class UserModel(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    reset_password_question = db.Column(db.String(255), nullable=True)
    reset_password_answer = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)
    bio = db.Column(db.String(300), nullable=True)
    location = db.Column(db.String(30), nullable=True)
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

    likes = db.relationship("LikeModel", back_populates="users")
    comments = db.relationship("CommentModel", back_populates="users")
    rates = db.relationship("RateModel", back_populates="users")
    socials = db.relationship("SocialModel", back_populates="users")
    follower = db.relationship(
        "FollowingModel",
        back_populates="follower_users",
        foreign_keys="[FollowingModel.follower_id]",
    )
    followed = db.relationship(
        "FollowingModel",
        back_populates="followed_users",
        foreign_keys="[FollowingModel.followed_id]",
    )

    def __init__(
        self,
        username,
        first_name,
        last_name,
        email,
        password,
        reset_password_question,
        reset_password_answer,
        image,
        role,
        bio,
        location,
        view_count,
    ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.reset_password_question = reset_password_question
        self.reset_password_answer = reset_password_answer
        self.image = image
        self.role = role
        self.bio = bio
        self.location = location
        self.view_count = view_count

    def add_user(self):
        try:
            self.validate_email()
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_user(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        if user is None:
            logging.error(f"User with id {user_id} not found.")
            abort(404, f"User with id {user_id} not found.")
        return user

    def update_user(self, user_data):
        for key, value in user_data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(email_regex, email) is not None

    def validate_email(self):
        if not self.is_valid_email(self.email):
            raise ValueError("Invalid email format")
