from typing import Generator

from flask import Flask
from flask.testing import FlaskClient

import pytest

from flaskr import create_app
from flaskr.extensions import bcrypt_ext
from flaskr.extensions import db
from flaskr.core import test_settings
from flaskr.entity import User
from flaskr.repository import user_repository


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app(test_settings)

    with app.app_context():
        user_repository.add(
            User(
                email="unconfirmeduser@gmail.com",
                password="unconfirmed",
            )
        )
        user_repository.add(
            User(
                email="confirmeduser@gmail.com",
                password="confirmed",
                is_confirmed=True,
            )
        )

        yield app

        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
