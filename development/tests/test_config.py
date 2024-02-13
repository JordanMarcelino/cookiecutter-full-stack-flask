import os
import pytest

os.environ["POSTGRES_HOST"] = "db"
from flaskr.core import logger
from flaskr.core import settings


def test_flask_config():
    assert settings.FLASK_APP == "flaskr"
    assert settings.FLASK_ENV == "development"
    assert len(settings.SECRET_KEY) == 22


def test_postgres_config():
    assert settings.POSTGRES_HOST == "localhost"
    assert settings.SQLALCHEMY_DATABASE_URI is not None


def test_jwt_config():
    assert settings.JWT_COOKIE_SECURE is False
    assert len(settings.JWT_SECRET_KEY) == 22
    assert settings.JWT_TOKEN_LOCATION == ["cookies", "headers"]
