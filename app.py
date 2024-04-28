import os
from flask import Flask, jsonify
from flask_smorest import Api
from dotenv import load_dotenv
from db import db
from psycopg2 import _psycopg
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import sentry_sdk
import logging

# from json_encoder import CustomJSONEncoder
from controllers import (
    users_blueprint,
    recipes_blueprint,
    user_socials_blueprint,
    instructions_blueprint,
)


# Sentry
sentry_sdk.init(
    dsn="https://affc2afb70a92276512c6b814dbaba50@o4507121964744704.ingest.de.sentry.io/4507121968480336",
    # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    profiles_sample_rate=1.0,
)


def create_app(is_test=False):
    app = Flask(__name__)
    load_dotenv()

    # app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    # app.json_encoder = CustomJSONEncoder

    app.config.update(
        API_TITLE="HealtHub",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.2",
        OPENAPI_SWAGGER_UI_PATH="/swagger",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        OPENAPI_URL_PREFIX="/",
    )

    app.config["SQLALCHEMY_ECHO"] = True

    if is_test is True:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URI", "sqlite:///data.db"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # class SupaUser(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String(80), unique=True, nullable=False)
    #     email = db.Column(db.String)

    # with app.app_context():
    #     db.create_all()

    Migrate(app, db)

    app.config["DEBUG"] = True

    jwt = JWTManager(app)

    app.config["JWT_SECRET_KEY"] = "Tim Depok RevoU"
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
    api.register_blueprint(users_blueprint)
    api.register_blueprint(recipes_blueprint)
    api.register_blueprint(user_socials_blueprint)
    api.register_blueprint(instructions_blueprint)

    # Logging configuration
    logging.basicConfig(level=logging.ERROR)

    # Logging example
    app.logger.error("An unexpected error occurred")

    return app
