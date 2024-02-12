import pytest

from flaskr.core import settings, logger


def test_flask_config():
    assert settings.FLASK_APP == "flaskr"
    assert settings.FLASK_ENV == "development"
    assert len(settings.SECRET_KEY) == 32


def test_postgres_config():
    assert settings.POSTGRES_HOST == "localhost"
    assert settings.SQLALCHEMY_DATABASE_URI is not None
