from flask import Flask

from flaskr.forms import LoginForm
from flaskr.forms import RegisterForm


def test_register_validate_success(app: Flask):
    form = RegisterForm(email="success@gmail.com", password="secret", confirm="secret")

    assert form.validate() is True


def test_register_validate_invalid_email_format(app: Flask):
    form = RegisterForm(email="success", password="secret", confirm="")

    assert form.validate() is False


def test_register_validate_invalid_confirm_password(app: Flask):
    form = RegisterForm(email="success@gmail.com", password="secret", confirm="")

    assert form.validate() is False


def test_register_validate_email_already_registered(app: Flask):
    form = RegisterForm(
        email="unconfirmeduser@gmail.com", password="secret", confirm="secret"
    )

    assert form.validate() is False


def test_login_validate_success(app: Flask):
    form = LoginForm(email="unconfirmeduser@gmail.com", password="unconfirmed")

    assert form.validate() is True


def test_login_validate_invalid_email_format(app: Flask):
    form = LoginForm(email="unconfirmeduser", password="unconfirmed")

    assert form.validate() is False
