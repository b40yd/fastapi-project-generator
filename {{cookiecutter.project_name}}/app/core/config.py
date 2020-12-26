#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


import hashlib
import logging
import sys
from typing import List

from loguru import logger
from pydantic import BaseSettings

from app.core.logging import InterceptHandler

hash = hashlib.sha512()
hash.update('info-leak-monitor'.encode('utf-8'))


class Settings(BaseSettings):

    jwt_token_prefix: str = "token"  # noqa: s105
    version: str = "0.0.0"

    debug: bool = False
    log_file: str = 'info.log'

    database_url: str = "sqlite:///info-leak-monitor.sqlite?charset=utf8mb4&check_same_thread=false"

    database_echo: bool = False

    secret_key: str = hash.hexdigest()
    access_token_expire: int = 60 * 60 * 24 * 7

    apscheduler_max_instances: int = 10

    project_name: str = "fastapi example application"
    api_prefix: str = "/api"
    allowed_hosts: List[str] = ['*']

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()

LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(
    handlers=[{"sink": settings.log_file, "level": LOGGING_LEVEL}])
logger.add(settings.log_file, rotation="00:00")
