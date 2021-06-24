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
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if not db is None:
            db.close()
