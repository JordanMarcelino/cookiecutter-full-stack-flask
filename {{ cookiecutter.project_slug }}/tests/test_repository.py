from uuid import uuid4

from flask import Flask
from flaskr.entity import User
from flaskr.extensions import bcrypt_ext
from flaskr.repository import user_repository

import pytest

from werkzeug.exceptions import NotFound


def test_add_entity_success(app: Flask):
    email, password = "test@gmail.com", "secret"

    new_user = User(
        email=email, password=bcrypt_ext.generate_password_hash(password).decode("utf8")
    )
    user_repository.add(new_user)

    existing_user = user_repository.get_by_email(email)

    assert new_user.id == existing_user.id
    assert new_user.email == existing_user.email == email
    assert bcrypt_ext.check_password_hash(existing_user.password, password) is True


def test_get_by_id_success(app: Flask):
    email, password = "test@gmail.com", "secret"

    new_user = User(
        email=email, password=bcrypt_ext.generate_password_hash(password).decode("utf8")
    )
    user_repository.add(new_user)

    existing_user = user_repository.get(new_user.id)

    assert new_user.id == existing_user.id
    assert new_user.email == existing_user.email == email
    assert bcrypt_ext.check_password_hash(existing_user.password, password) is True


def test_get_by_id_failed(app: Flask):
    with pytest.raises(NotFound):
        id = uuid4()
        _ = user_repository.get(id)


def test_check_password_success(app: Flask):
    user = user_repository.get_by_email("unconfirmeduser@gmail.com")

    assert user.email == "unconfirmeduser@gmail.com"
    assert bcrypt_ext.check_password_hash(user.password, "unconfirmed") is True
