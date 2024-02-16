from uuid import uuid4

from flask_login import UserMixin

from pendulum import now

from sqlalchemy import BigInteger
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from flaskr.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[Uuid] = mapped_column(
        Uuid(as_uuid=True), nullable=False, default=uuid4, primary_key=True
    )
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[int] = mapped_column(
        BigInteger(), nullable=False, default=lambda _: now().int_timestamp
    )
    updated_at: Mapped[int] = mapped_column(
        BigInteger(), nullable=False, default=lambda _: now().int_timestamp
    )
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_confirmed: Mapped[bool] = mapped_column(nullable=False, default=False)
    confirmed_at: Mapped[int] = mapped_column(BigInteger(), nullable=True)

    def __repr__(self) -> str:
        return f"<email {self.email}>"
