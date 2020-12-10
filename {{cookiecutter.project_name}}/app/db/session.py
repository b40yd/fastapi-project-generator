#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from app.core.config import DATABASE_ECHO, DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL, echo=DATABASE_ECHO, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
