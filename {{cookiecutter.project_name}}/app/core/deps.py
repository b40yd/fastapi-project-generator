#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from typing import Generator

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.token import TokenData
from fastapi import Header, HTTPException
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def verify_token(security_scopes: SecurityScopes,
                       x_token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="401 unauthorized",
    )

    try:
        payload = jwt.decode(x_token, settings.secret_key)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, subject=username)
    except (JWTError, AttributeError):
        raise credentials_exception

    flag = False
    for scope in security_scopes.scopes:
        if scope in token_data.scopes:
            flag = True
            break

    if not flag:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )
