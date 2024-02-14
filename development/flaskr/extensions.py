import bcrypt

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from flask_jwt_extended import JWTManager

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
