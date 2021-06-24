#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserRegister

from . import Repository


class UserRepository(Repository):
    def create(self, userinfo: UserRegister) -> User:
        password = get_password_hash(userinfo.password)
        user = User()
        user.username = userinfo.username
        user.password = password
        user.email = userinfo.email
        self.db.add(user)
        self.db.commit()
        return user

    def authenticate(self, username: str, password: str) -> User:
        user = self.get_by_username(username)

        if not user:
            return False

        if not verify_password(password, user.password):
            return False

        return user

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
