#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
