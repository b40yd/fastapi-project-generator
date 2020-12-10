#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from app.core.config import SECRET_KEY
from app.core.deps import get_db
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserInfo, UserRegister
from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session


async def get_current_user(x_token: str = Header(None),
                           db: Session = Depends(get_db)) -> UserInfo:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": ""},
    )
    try:
        payload = jwt.decode(x_token, SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = UserRepository.get_by_username(db, username)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user


class UserRepository():

    @classmethod
    def create(self, db: Session, userinfo: UserRegister) -> Token:
        password = get_password_hash(userinfo.password)

        user = self.get_by_username(db, userinfo.username)
        if not user:
            user = User()
            user.username = userinfo.username
            user.password = password
            user.email = userinfo.email
            db.add(user)
            db.commit()
        return user

    @classmethod
    def authenticate(self, db: Session, username: str, password: str) -> User:
        user = self.get_by_username(db, username)

        if not user:
            return False

        if not verify_password(password,
                               user.password):
            return False

        return user

    @classmethod
    def get_by_username(self, db: Session, username: str) -> User:
        return db.query(User).filter(
            User.username == username
        ).first()

    @classmethod
    def get_by_email(self,  db: Session, email: str) -> User:
        return db.query(User).filter(
            User.email == email
        ).first()
