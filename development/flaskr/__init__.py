from flask import Flask

from pydantic_settings import BaseSettings

from flaskr.core import logger
from flaskr.core import DevelopmentSettings
from flaskr.extensions import csrf
from flaskr.extensions import db
from flaskr.extensions import jwt


def create_app(config: BaseSettings = DevelopmentSettings()) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    logger.debug(app.config)

    with app.app_context():
        csrf.init_app(app)
        db.init_app(app)
        jwt.init_app(app)

        db.create_all()

    @app.route("/")
    def root():
        return "Hello world"

    return app
