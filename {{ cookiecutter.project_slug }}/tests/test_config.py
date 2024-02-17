import pytest

from flaskr.core import dev_settings
from flaskr.core import Settings


@pytest.fixture
def settings() -> Settings:
    return dev_settings


def test_flask_config(settings: Settings):
    assert settings.FLASK_APP == "flaskr"
    assert settings.API_V1_STR == "/api/v1"
    assert len(settings.SECRET_KEY) == 22
    assert settings.DEBUG is True
    assert settings.DEVELOPMENT is True


def test_postgres_config(settings: Settings):
    assert settings.POSTGRES_HOST == "localhost"
    assert settings.SQLALCHEMY_DATABASE_URI is not None


def test_jwt_config(settings: Settings):
    assert settings.JWT_COOKIE_SECURE is False
    assert len(settings.JWT_SECRET_KEY) == 22
    assert settings.JWT_TOKEN_LOCATION == ["cookies", "headers"]


def test_bcrypt_config(settings: Settings):
    assert settings.BCRYPT_LOG_ROUNDS == 13


def test_wtf_config(settings: Settings):
    assert settings.WTF_CSRF_ENABLED is False


def test_mail_config(settings: Settings):
    assert settings.MAIL_USE_SSL is True
    assert settings.MAIL_USERNAME is not None
    assert settings.MAIL_PASSWORD is not None
    assert settings.MAIL_PORT == 465
