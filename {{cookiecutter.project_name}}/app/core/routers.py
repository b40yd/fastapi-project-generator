#
# Copyright (C) 2020, {{cookiecutter.author}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from app.api import home
from fastapi import APIRouter

router = APIRouter()
router.include_router(home.router, tags=["home"])
