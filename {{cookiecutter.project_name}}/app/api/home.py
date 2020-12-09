#
# Copyright (C) 2020, {{cookiecutter.author}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.deps import get_db, get_scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

router = APIRouter()


async def hello_task():
    logger.info("hello task....")


@router.get("/")
async def home(db: Session = Depends(get_db),
               scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
    # scheduler.add_job(hello_task, 'interval', seconds=3)
    return {"router": "/"}


@router.get("/add/test")
async def test_add(db: Session = Depends(get_db),
                   scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
    job = scheduler.add_job(hello_task, 'interval', seconds=3)
    return {"id": job.id}


@router.get("/tasks")
async def get_tasks(db: Session = Depends(get_db),
                    scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
    jobs = scheduler.get_jobs()
    rst = []
    for job in jobs:
        rst.append({"id": job.id})
    return rst


@router.get("/del/{id}")
async def del_task(id: str,
                   db: Session = Depends(get_db),
                   scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
    scheduler.remove_job(id)
    return {"id": id}
