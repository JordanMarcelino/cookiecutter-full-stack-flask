from typing import List

import pendulum

from .repository import Repository
from flaskr.entity import User
from flaskr.extensions import bcrypt_ext
from flaskr.extensions import db


class UserRepository(Repository[User]):
    def get(self, id: str) -> User:
        return User.query.filter(User.id == id).first_or_404()

    def get_by_email(self, email: str) -> User:
        return User.query.filter(User.email == email).first_or_404()

    def get_all(self) -> List[User]:
        pass

    def add(self, entity: User) -> None:
        db.session.add(entity)
        db.session.commit()

    def update(self, entity: User, password: str = None) -> None:
        user: User = User.query.filter(User.id == entity.id).first_or_404()

        if entity.email != "":
            user.email = entity.email

        if password is not None:
            user.password = bcrypt_ext.generate_password_hash(password).decode("utf8")

        user.updated_at = pendulum.now().int_timestamp

        db.session.add(user)
        db.session.commit()

    def delete(self, id: str) -> None:
        pass


user_repository = UserRepository()
