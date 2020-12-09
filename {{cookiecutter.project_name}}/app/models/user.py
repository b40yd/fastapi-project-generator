#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.db.base import Base
from loguru import logger
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False, unique=True)

    @classmethod
    def get_by_username(cls, db: Session, username: str):
        logger.info("========={0}", db)
        data = db.query(cls).filter_by(username=username).first()

        return data
