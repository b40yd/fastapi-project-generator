#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.config import settings
from app.core.http_error import http_error_handler
from app.core.routers import router as api_router
from app.core.validation_error import http422_error_handler
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
        docs_url=settings.docs_url,
        openapi_url=settings.openapi_url,
        redoc_url=settings.redoc_url,
        version=settings.version,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError,
                                      http422_error_handler)

    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = get_application()
