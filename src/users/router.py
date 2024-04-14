from fastapi import APIRouter, Depends, HTTPException

from src.exceptions.NoUserException import NoUserException
from src.exceptions.WrongPasswordException import WrongPasswordException

from src.database import DBSession
from src.dependencies import get_db_session
from src.users.schemas.User import User
from src.users.schemas.UserToken import UserToken
from src.users.schemas.UserCreate import UserCreate
from src.users.schemas.UserPassword import UserPassword
from src.users.crud import (
    create_user as create_db_user,
    signin_user as signin_db_user,
    remove_user as remove_db_user,
    get_user as get_db_user
)


user_router = APIRouter()


@user_router.post("/users/signup", response_model=UserToken)
def create_user(user: UserCreate, db: DBSession = Depends(get_db_session)):
    from main import special_token as app_token

    if get_db_user(db, login=user.login):
        raise HTTPException(status_code=404, detail=f"User with login '{user.login}' is already exists.")

    if user.is_admin and user.admin_token != app_token():
        raise HTTPException(status_code=404, detail=f"Entered wrong admin-token '{user.admin_token}'.")

    return create_db_user(db, user)


@user_router.post("/users/signin", response_model=UserToken)
def signin_user(user: UserPassword, db: DBSession = Depends(get_db_session)):
    user_db = get_user(user.login, db)

    if not signin_db_user(user, user_db):
        raise WrongPasswordException(user.login)

    return user_db


@user_router.post("/users/remove", response_model=bool)
def remove_user(user: UserPassword, db: DBSession = Depends(get_db_session)):
    user_db = get_user(user.login, db)

    if not signin_db_user(user, user_db):
        raise WrongPasswordException(user.login)

    return remove_db_user(user_db)


@user_router.get("/users/get", response_model=User)
def get_user(login: str, db: DBSession = Depends(get_db_session)):
    db_user = get_db_user(db, login=login)
    if db_user is None:
        raise NoUserException(login)
    return db_user
