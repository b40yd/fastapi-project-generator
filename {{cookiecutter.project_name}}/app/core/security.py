#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

import time
from typing import Dict

from app.core.config import settings
from passlib.context import CryptContext
from app.core.config import settings
from app.schemas.token import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError

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


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.jwt_token_prefix.lower(),
    scopes={
        "api": "Read information about the current API.",
        # "items": "Read items."
    },
)


async def verify_access_token(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
) -> str:
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
        username: str = payload.get("sub", None)
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, subject=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    flag = False
    for scope in security_scopes.scopes:
        if scope in token_data.scopes:
            flag = True
            break

    if not flag:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return username
