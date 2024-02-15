from time import time_ns
from typing import List

from flask import abort

from .repository import Repository
from flaskr.entity import User
from flaskr.extensions import bcrypt_ext
from flaskr.extensions import db


class UserRepository(Repository[User]):
    def get(self, email: str) -> User:
        return User.query.filter(User.email == email).first_or_404()

    def get_all(self) -> List[User]:
        pass

    def add(self, entity: User) -> None:
        entity.password = bcrypt_ext.generate_password_hash(entity.password)

        db.session.add(entity)
        db.session.commit()

    def update(self, entity: User) -> None:
        user: User = User.query.filter(User.id == entity.id).first_or_404()

        if not bcrypt_ext.check_password_hash(user.password, entity.password):
            abort(401)

        user.email = entity.email
        user.password = bcrypt_ext.generate_password_hash(entity.password)
        user.updated_at = time_ns()

        db.session.add(user)
        db.session.commit()

    def delete(self, id: str) -> None:
        pass


user_repository = UserRepository()
