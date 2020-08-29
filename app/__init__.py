import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

import connexion
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app import encoder
from config import Config


jwt = JWTManager()


def create_app(config_class=Config):

    connexion_app: connexion.App = connexion.App(
        __name__, specification_dir="./api/openapi_spec"
    )

    app = connexion_app.app
    app.json_encoder = encoder.JSONEncoder

    connexion_app.add_api(
        "v0_1.yaml", arguments={"title": "solverstack Vrp"}, pythonic_params=True
    )

    app.config.from_object(config_class)

    CORS(app)
    jwt.init_app(app)

    from app.api.v0_1 import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api/v0.1")

    return app
