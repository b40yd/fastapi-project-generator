#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    (f"{{cookiecutter.database_driver}}://{settings.database_username}:{settings.database_password}@"
     f"{settings.database_host}:{settings.database_port}/{settings.database_name}?charset=utf8mb4"
     ),
    echo=settings.database_echo,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine)
