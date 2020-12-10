#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#


from app.core.deps import get_db
from app.core.security import create_access_token
from app.repositories.user import UserRepository, get_current_user
from app.schemas.user import UserAuth, UserInfo, UserRegister, UserToken
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

router = APIRouter()
# async def hello_task():
#     logger.info("hello task....")


@router.post("/register", response_model=UserToken)
async def register(userinfo: UserRegister,
                   db: Session = Depends(get_db)):
    user = UserRepository.create(db, userinfo)
    if user:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="'{0}' existed, register failed. ".format(
                userinfo.username),
        )
    access_token = create_access_token(user.username)
    return {
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=UserToken)
async def login_for_access_token(userinfo: UserAuth,
                                 db: Session = Depends(get_db)):

    user = UserRepository.authenticate(db,
                                       userinfo.username,
                                       userinfo.password)

    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.username)
    return {
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserInfo)
async def info(current_user: UserInfo = Depends(get_current_user)):
    # return {"username": current_user.username, "email": current_user.email}
    return current_user

# @ router.get("/")
# async def home(db: Session = Depends(get_db),
#                scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
#     # scheduler.add_job(hello_task, 'interval', seconds=3)
#     return {"router": "/"}


# @ router.get("/add/test")
# async def test_add(db: Session = Depends(get_db),
#                    scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
#     job = scheduler.add_job(hello_task, 'interval', seconds=3)
#     return {"id": job.id}


# @ router.get("/tasks")
# async def get_tasks(db: Session = Depends(get_db),
#                     scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
#     jobs = scheduler.get_jobs()
#     rst = []
#     for job in jobs:
#         rst.append({"id": job.id})
#     return rst


# @ router.get("/del/{id}")
# async def del_task(id: str,
#                    db: Session = Depends(get_db),
#                    scheduler: AsyncIOScheduler = Depends(get_scheduler)) -> dict:
#     scheduler.remove_job(id)
#     return {"id": id}
