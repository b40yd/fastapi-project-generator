#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from datetime import datetime, timedelta
from typing import Dict, Optional

from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext

JWT_SUBJECT = "{{cookiecutter.project_name}}"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_jwt_token(
        jwt_content: Dict[str, str],
        secret_key: str,
        expires_delta: Optional[timedelta] = None,
):
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key)


def create_access_token(username: str,):
    return create_jwt_token(
        jwt_content={"sub": username},
        secret_key=settings.SECRET_KEY,
        expires_delta=timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE)
    )
