#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.deps import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class Repository:
    db: Session

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
