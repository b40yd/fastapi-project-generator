#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.db.base import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    email = Column(String(32), nullable=True, unique=True)
