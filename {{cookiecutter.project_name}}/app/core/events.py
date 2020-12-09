#
# Copyright (C) 2020, {{cookiecutter.author}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from typing import Callable

from app.core.config import DATABASE_URL
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from loguru import logger


async def start_scheduler(app: FastAPI) -> None:
    logger.info("APScheduler Starting", repr(DATABASE_URL))
    jobstores = {
        'default': SQLAlchemyJobStore(url=DATABASE_URL)
    }
    app.scheduler = AsyncIOScheduler()
    app.scheduler.configure(jobstores=jobstores)

    app.scheduler.start()
    logger.info("APScheduler established")


async def stop_scheduler(app: FastAPI) -> None:
    logger.info("APScheduler Closing")

    await app.scheduler.close()

    logger.info("APScheduler closed")


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await start_scheduler(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await stop_scheduler(app)

    return stop_app
