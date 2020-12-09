#
# Copyright (C) 2020, 7ym0n.q6e
#
# Author: 7ym0n.q6e <bb.qnyd@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from typing import Callable

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from loguru import logger

from app.core.config import DATABASE_URL


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
