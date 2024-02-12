from flask import Flask
from pydantic_settings import BaseSettings

from flaskr.core import logger
from flaskr.core import settings


def create_app(config: BaseSettings = settings) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    logger.debug(app.config)

    with app.app_context():
        pass

    @app.route("/")
    def root():
        return "Hello world"

    return app
