import os
from flask import Flask, jsonify
from flask_smorest import Api
from dotenv import load_dotenv
from db import db
from psycopg2 import _psycopg
from flask_jwt_extended import JWTManager


def create_app(is_test=False):
    app = Flask(__name__)
    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

    db.init_app(app)

    # class SupaUser(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String(80), unique=True, nullable=False)
    #     email = db.Column(db.String)

    with app.app_context():
        db.create_all()

    app.config["DEBUG"] = True

    jwt = JWTManager(app)

    app.config["JWT_SECRET_KEY"] = "tet tet toooettt 1000x"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 36000  #  Expires in 10 hours
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 2592000  #  Expires in 30 days

    @jwt.expired_token_loader
    def expired_token_callback(expired_token, jwt_data):
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(_):
        return jsonify({"message": "Invalid token"}), 400

    @jwt.unauthorized_loader
    def unauthorized_callback(_):
        return jsonify({"message": "Unauthorized access"}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(_):
        return jsonify({"message": "Fresh token required"}), 401

    api = Api(app)

    return app
