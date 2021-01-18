#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

import hashlib
import logging
from typing import List

from app.core.logging import InterceptHandler
from loguru import logger
from pydantic import BaseSettings

hash = hashlib.sha512()
hash.update('info-leak-monitor'.encode('utf-8'))


class Settings(BaseSettings):
    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"  # noqa: S105
    version: str = "0.0.0"

    debug: bool = False

    database_url: str = 'sqlite:///info-leak-monitor.sqlite?charset=utf8mb4&check_same_thread=false'
    database_echo: bool = False

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    redis_password: str = ''

    secret_key: str = hash.hexdigest()
    access_token_expire: int = 60 * 60 * 24 * 7

    apscheduler_max_instances: int = 10

    project_name: str = "info-monitor"
    allowed_hosts: List[str] = ['*']

    gitlab_repository: str = "https://gitlab.com"

    log_file: str = "info.log"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
# logging configuration

LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.ERROR
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(
    handlers=[{
        "sink": settings.log_file,
        "level": LOGGING_LEVEL,
        "rotation": "00:00",
        "retention": '10 days',
        "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    }])
