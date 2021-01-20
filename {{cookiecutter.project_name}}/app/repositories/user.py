#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.config import settings
from app.core.deps import get_db
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.token import Token, TokenData
from app.schemas.user import UserInfo, UserRegister
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.jwt_token_prefix.lower(),
    scopes={
        "me": "Read information about the current user.",
        # "items": "Read items."
    },
)


async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> UserInfo:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token,
                             settings.secret_key,
                             algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, subject=username)
        user = UserRepository.get_by_username(db, username)
        if user is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: UserInfo = Security(
    get_current_user, scopes=["me"])):

    return current_user


class UserRepository:
    @classmethod
    def create(self, db: Session, userinfo: UserRegister) -> Token:
        password = get_password_hash(userinfo.password)
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

        if not verify_password(password, user.password):
            return False

        return user

    @classmethod
    def get_by_username(self, db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    @classmethod
    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()
