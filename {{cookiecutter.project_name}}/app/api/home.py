#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

from app.core.config import settings
from app.core.deps import get_db
from app.core.security import create_access_token
from app.repositories.user import UserRepository, get_current_active_user
from app.schemas.user import UserInfo, UserRegister, UserToken
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

router = APIRouter()


@router.post("/register", response_model=UserToken)
async def register(userinfo: UserRegister, db: Session = Depends(get_db)):
    user = UserRepository.get_by_username(db, userinfo.username)
    if user:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="'{0}' existed, register failed. ".format(
                userinfo.username),
        )
    else:
        user = UserRepository.create(db, userinfo)
    access_token = create_access_token(user.username)
    return {
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "token_type": settings.jwt_token_prefix,
    }


@router.post("/login", response_model=UserToken)
async def login_for_access_token(
        userinfo: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):

    user = UserRepository.authenticate(db, userinfo.username,
                                       userinfo.password)

    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": settings.jwt_token_prefix},
        )
    access_token = create_access_token(user.username)
    return {
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "token_type": settings.jwt_token_prefix,
    }


@router.get("/me", response_model=UserInfo)
async def info(current_user: UserInfo = Depends(get_current_active_user)):
    return current_user
