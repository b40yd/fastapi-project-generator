#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    subject: Union[str, Any]
    scopes: List[str] = []
