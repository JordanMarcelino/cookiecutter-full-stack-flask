from datetime import datetime
from datetime import timedelta

import bcrypt

from flask import Flask
from flask import Response

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies

from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import CSRFProtect

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


bcrypt_ext = Bcrypt()

csrf = CSRFProtect()

db = SQLAlchemy(model_class=Base)

jwt = JWTManager()

login_manager = LoginManager()

mail = Mail()


def refresh_expiring_jwts(response: Response) -> Response:
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
