#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from typing import Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str
    email: Optional[str]

    class Config:
        orm_mode = True


class UserRegister(UserInfo):
    password: str
