#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url, echo=settings.database_echo, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
