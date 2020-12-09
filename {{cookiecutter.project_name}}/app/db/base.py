#
# Copyright (C) 2020, {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.now,
                         server_default=func.now())
    update_time = Column(DateTime,
                         default=datetime.now,
                         onupdate=datetime.now,
                         server_default=func.now(),
                         server_onupdate=func.now())
    is_delete = Column(Integer, default=0)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        import re
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        return "_".join(name_list).lower()
