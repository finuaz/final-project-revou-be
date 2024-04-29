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
from flask_cors import CORS
from extensions import cache

from controllers import (
    users_blueprint,
    recipes_blueprint,
    user_socials_blueprint,
    instructions_blueprint,
    feeds_blueprint,
)


# Sentry
sentry_sdk.init(
    dsn="https://affc2afb70a92276512c6b814dbaba50@o4507121964744704.ingest.de.sentry.io/4507121968480336",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


def create_app(is_test=False):
    app = Flask(__name__)
    load_dotenv()

    # Load common configuration settings from config.py
    app.config.from_pyfile("config.py")

    # Override configuration settings as needed
    app.config.update(
        API_TITLE="HealtHub",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.2",
        OPENAPI_SWAGGER_UI_PATH="/swagger",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        OPENAPI_URL_PREFIX="/",
        SQLALCHEMY_ECHO=True,
        DEBUG=True,
    )

    if is_test is True:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URI", "sqlite:///data.db"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize cache with app
    cache.init_app(app)

    # Initialize database
    db.init_app(app)
    Migrate(app, db)

    # Enable CORS
    CORS(app)

    # JWT configuration
    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = "Tim Depok RevoU"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 36000  #  Expires in 10 hours
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 2592000  #  Expires in 30 days

    # JWT error handlers
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

    # Blueprints for controllers
    api = Api(app)
    api.register_blueprint(users_blueprint)
    api.register_blueprint(recipes_blueprint)
    api.register_blueprint(user_socials_blueprint)
    api.register_blueprint(instructions_blueprint)
    api.register_blueprint(feeds_blueprint)

    # Logging configuration
    logging.basicConfig(level=logging.ERROR)

    # Logging example
    app.logger.error("An unexpected error occurred")

    return app
