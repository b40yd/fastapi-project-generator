#
# Copyright (C) 2020, {{cookiecutter.author}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from typing import Generator

from app.db.session import SessionLocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from starlette.requests import Request


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_scheduler(request: Request) -> AsyncIOScheduler:
    return request.app.scheduler
