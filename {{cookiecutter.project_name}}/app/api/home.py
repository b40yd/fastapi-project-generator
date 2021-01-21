#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.deps import get_db, verify_token
from app.core.security import create_access_token
from app.repositories.user import UserRepository, get_current_active_user
from app.schemas.token import Token
from app.schemas.user import UserInfo, UserRegister
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.orm import Session
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_500_INTERNAL_SERVER_ERROR)

router = APIRouter()


@router.post("/register", response_model=UserInfo)
async def register(userinfo: UserRegister, db: Session = Depends(get_db)):
    try:
        user = UserRepository.get_by_username(db, userinfo.username)
        if user:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="'{0}' existed, register failed. ".format(
                    userinfo.username),
            )
        else:
            user = UserRepository.create(db, userinfo)

        return {
            "username": user.username,
            "email": user.email,
        }

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


@router.get("/me", response_model=UserInfo)
async def info(current_user: UserInfo = Depends(get_current_active_user)):
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    try:
        user = UserRepository.authenticate(db, form_data.username,
                                           form_data.password)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")

    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = create_access_token(data={
        "sub": user.username,
        "scopes": form_data.scopes
    })
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/status", dependencies=[Security(verify_token, scopes=["api"])])
async def get_status():
    return {"status": "ok"}
