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
async def create_user(user: UserCreate, db: DBSession = Depends(get_db_session)):
    """
    If gotten user's login is unique and admin token is valid (only if param is_admin is true), user will be added
    into database.

    :param user: schema with user's login, password, is_admin and extra param admin_token
    :type user: UserCreate

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: dict with new id, login, token and is_admin
    :rtype: dict

    :raises UserException
    """
    from src.secret import check_admin_token

    if get_db_user(db, login=user.login.lower()):
        raise UserException.user_exists(user.login.lower())

    if user.is_admin and not check_admin_token(user.admin_token):
        raise UserException.wrong_admin_token(user.admin_token)

    return create_db_user(db, user)


@users_router.post(f"{router_name}/signin", response_model=UserToken)
async def signin_user(user: UserPassword, db: DBSession = Depends(get_db_session)):
    """
    Checks validity of gotten login and password. If they are valid, will return access token of user.

    :param user: schema with login and password.
    :type user: UserPassword

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: dict with id, login, token and is_admin
    :rtype: dict

    :raises UserException
    """
    user_db = get_user(login=user.login.lower(), db=db)

    if not signin_db_user(user, user_db):
        raise UserException.wrong_password(user.login.lower())

    return user_db


@users_router.post(f"{router_name}/remove", response_model=bool)
async def remove_user(user: UserPassword, db: DBSession = Depends(get_db_session)):
    """
    Checks validity of gotten login and password. If they are valid, will mark record in db as deleted.

    :param user: schema with login and password
    :type user: UserPassword

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: true if user is finally deleted
    :rtype: bool

    :raises UserException
    """

    user_db = get_user(login=user.login.lower(), db=db)

    if not signin_db_user(user, user_db):
        raise UserException.wrong_password(user.login.lower())

    return remove_db_user(db, user_db)


@users_router.post(f"{router_name}/change", response_model=UserToken)
async def change_user(user: UserChange, db: DBSession = Depends(get_db_session)):
    """
    If gotten login and password are valid, they will be changed on gotten new login and password.

    :param user: schema with login and password, new login and password
    :type user: UserChange

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: dict with id, login, token and is_admin
    :rtype: dict

    :raises UserException
    """
    user_db = get_user(login=user.login.lower(), db=db)

    if not signin_db_user(user, user_db):
        raise UserException.wrong_password(user.login.lower())

    return change_user_fields(db, user_db, user)


@users_router.get(f"{router_name}/get", response_model=User)
def get_user(id: int, login: str = None, token: str = None, db: DBSession = Depends(get_db_session)):
    """
    Finds user with gotten either login or token and return his model.

    :param id: user's id
    :type id: int

    :param login: user's login
    :type login: str or None

    :param token: user's token
    :type token: str or None

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: schema with user's id, login and is_admin
    :rtype: User

    :raises UserException
    """
    db_user = get_db_user(db, id=id, login=login, token=token)

    if db_user is None:
        raise UserException.no_user(login=login, token=token)

    return db_user


@users_router.get(f"{router_name}/is_admin", response_model=bool)
def is_user_admin(id: int, login: str = None, token: str = None, db: DBSession = Depends(get_db_session)):
    """
    Finds user with gotten either login or token and return true if he's admin.

    :param id: user's id
    :type id: int

    :param login: user's login
    :type login: str or None

    :param token: user's token
    :type token: str or None

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: true if user is admin
    :rtype: bool

    :raises UserException
    """
    db_user = get_user(id, login, token, db)

    if not db_user.is_admin:
        raise UserException.is_not_admin(login=login, token=token)

    return True
