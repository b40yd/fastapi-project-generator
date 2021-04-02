#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.config import Settings
from sqlalchemy.orm import Session


class Service:
    db: Session
    config: Settings

    def __init__(self, db: Session, config: Settings):
        self.db = db
        self.config = config
