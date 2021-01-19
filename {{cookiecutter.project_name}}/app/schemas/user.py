#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from typing import Optional

from app.schemas.token import Token
from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    email: Optional[str]

    class Config:
        orm_mode = True


class UserToken(UserInfo, Token):
    pass


class UserRegister(UserInfo):
    password: str
