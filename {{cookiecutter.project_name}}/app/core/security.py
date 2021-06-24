#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

import time
from typing import Dict

from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_jwt_token(
    jwt_content: Dict,
    secret_key: str,
    expires_delta: int = 3600 * 24,
):
    to_encode = jwt_content.copy()
    expire = int(time.time()) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=settings.algorithm)


def create_access_token(data: Dict):
    return create_jwt_token(
        jwt_content=data,
        secret_key=settings.secret_key,
        expires_delta=settings.access_token_expire,
    )
