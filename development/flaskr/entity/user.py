from uuid import uuid4
from time import time_ns

from flask_login import UserMixin

from sqlalchemy import BigInteger
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from flaskr.extensions import bcrypt_ext
from flaskr.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[Uuid] = mapped_column(
        Uuid(as_uuid=True), nullable=False, default=uuid4, primary_key=True
    )
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[BigInteger] = mapped_column(
        BigInteger(), nullable=False, default=time_ns
    )
    updated_at: Mapped[BigInteger] = mapped_column(
        BigInteger(), nullable=False, default=time_ns
    )
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<email {self.email}>"
