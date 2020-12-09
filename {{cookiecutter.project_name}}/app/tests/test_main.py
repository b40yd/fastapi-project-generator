#
# Copyright (C) 2020, {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


import pytest
from app.main import app
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api")

    assert response.status_code == 200
