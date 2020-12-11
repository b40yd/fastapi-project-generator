#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


import hashlib
import logging
import sys
from typing import List

from app.core.logging import InterceptHandler
from loguru import logger
from pydantic import BaseSettings
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

hash = hashlib.sha512()
hash.update('info-leak-monitor'.encode('utf-8'))


class Settings(BaseSettings):
    API_PREFIX: str = "/api"

    JWT_TOKEN_PREFIX: str = "Token"  # noqa: S105
    VERSION: str = "0.0.0"

    config: Config = Config(".env")

    DEBUG: bool = config("DEBUG", cast=bool, default=False)

    DATABASE_URL: str = config(
        "DB_CONNECTION",
        default="sqlite:///info-leak-monitor.sqlite?charset=utf8mb4&check_same_thread=false")
    MAX_CONNECTIONS_COUNT: int = config(
        "MAX_CONNECTIONS_COUNT", cast=int, default=10)

    DATABASE_ECHO: bool = DEBUG

    SECRET_KEY: str = config("SECRET_KEY", default=hash.hexdigest())
    ACCESS_TOKEN_EXPIRE: int = 60 * 60 * 24 * 7

    APSCHEDULER_MAX_INSTANCES: int = config(
        "APSCHEDULER_MAX_INSTANCES", cast=int,  default=10)

    PROJECT_NAME: str = config(
        "PROJECT_NAME", default="FastAPI example application")
    ALLOWED_HOSTS: List[str] = config(
        "ALLOWED_HOSTS",
        cast=CommaSeparatedStrings,
        default=None,
    )


settings = Settings()