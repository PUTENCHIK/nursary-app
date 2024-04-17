from fastapi import APIRouter, Depends

from src.exceptions.UserException import UserException

from src.database import DBSession
from src.dependencies import get_db_session
from src.users.schemas.User import User
from src.users.schemas.UserToken import UserToken
from src.users.schemas.UserCreate import UserCreate
from src.users.schemas.UserPassword import UserPassword
from src.users.schemas.UserChange import UserChange
from src.users.crud import (
    create_user as create_db_user,
    signin_user as signin_db_user,
    remove_user as remove_db_user,
    change_user_fields,
    get_user as get_db_user
)


users_router = APIRouter()
router_name = "/users"


@users_router.post(f"{router_name}/signup", response_model=UserToken)
def create_user(user: UserCreate, db: DBSession = Depends(get_db_session)):
    from main import special_token as app_token

    if get_db_user(db, login=user.login):
        raise UserException.user_exists(user.login)

    if user.is_admin and user.admin_token != app_token():
        raise UserException.wrong_admin_token(user.admin_token)

    return create_db_user(db, user)


@users_router.post(f"{router_name}/signin", response_model=UserToken)
def signin_user(user: UserPassword, db: DBSession = Depends(get_db_session)):
    user_db = get_user(user.login, db)

    if not signin_db_user(user, user_db):
        raise UserException.wrong_password(user.login)

    return user_db


@users_router.post(f"{router_name}/remove", response_model=bool)
def remove_user(user: UserPassword, db: DBSession = Depends(get_db_session)):
    user_db = get_user(user.login, db)

    if not signin_db_user(user, user_db):
        raise UserException.wrong_password(user.login)

    return remove_db_user(user_db)


@users_router.post(f"{router_name}/change", response_model=UserToken)
def change_user(user: UserChange, db: DBSession = Depends(get_db_session)):
    user_db = get_user(user.login, db)

    if not signin_db_user(user, user_db):
        raise UserException.wrong_password(user.login)

    return change_user_fields(user_db, user)


@users_router.get(f"{router_name}/get", response_model=User)
def get_user(login: str, db: DBSession = Depends(get_db_session)):
    db_user = get_db_user(db, login=login)

    if db_user is None:
        raise UserException.no_user(login)

    return db_user
