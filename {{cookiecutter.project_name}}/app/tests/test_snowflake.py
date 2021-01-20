#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

import pytest
from app.utils.snowflake import SnowFlake


def test_snowflake_worker_id():
    sf = SnowFlake()
    assert 0 == sf.get_worker_id()


def test_snowflake_datacenter_id():
    sf = SnowFlake()
    assert 0 == sf.get_datacenter_id()
