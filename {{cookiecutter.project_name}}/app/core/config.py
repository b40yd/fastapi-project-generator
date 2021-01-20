#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

import logging
from typing import List, Optional, Union

from app.core.logging import InterceptHandler
from loguru import logger
from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress


class Settings(BaseSettings):
    project_name: str = "{{cookiecutter.project_name}}"
    allowed_hosts: List[str] = ["*"]
    api_prefix: str = "/api"

    version: str = "0.0.0"
    debug: bool = False

    docs_url: str = f"{api_prefix}/docs"
    openapi_url: str = f"{api_prefix}/openapi.json"
    redoc_url: str = f"{api_prefix}/redoc"

    jwt_token_prefix: str = "Token"
    algorithm: str = "HS256"
    secret_key: str = "{{cookiecutter.project_name}}_{{cookiecutter.author}}"
    access_token_expire: int = 60 * 60 * 24 * 7

    log_file: str = "info.log"

    database_username: str = "{{cookiecutter.database_username}}"
    database_password: str = "{{cookiecutter.database_password}}"
    database_host: Union[AnyHttpUrl,
                         IPvAnyAddress] = "{{cookiecutter.database_host}}"
    database_port: int = 3306
    database_name: str = "{{cookiecutter.database_name}}"

    database_url: str = (
        f"{{cookiecutter.database_driver}}://{database_username}:{database_password}@"
        f"{database_host}:{database_port}/{database_name}?charset=utf8mb4")
    database_echo: bool = False

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


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
        "retention": "10 days",
        "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    }])
