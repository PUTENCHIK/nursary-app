from sqlalchemy.orm import Session
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex

from src.users.models.User import User as UserModel
from src.users.schemas.UserPassword import UserPassword
from src.users.schemas.UserCreate import UserCreate
from src.users.schemas.UserChange import UserChange


def create_user(db: Session, user: UserCreate) -> Optional[UserModel]:
    """
    Gets new user's data and creates new record in database in table 'users'.

    :param db: database session
    :type db: Session

    :param user: user's schema with login, password, is_admin and admin_token
    :type user: UserCreate

    :return: user model from database
    :rtype: UserModel or None
    """
    pwd = generate_password_hash(user.password)

    db.user = UserModel(
        login=user.login.lower(),
        password=pwd,
        token=token_hex(8),
        is_admin=(user.is_admin and user.admin_token is not None),
        is_deleted=False
    )

    db.add(db.user)
    db.commit()
    db.refresh(db.user)

    return db.user


def signin_user(user: UserPassword, user_db: UserModel) -> bool:
    """
    Compares gotten password and password of database user.

    :param user: schema with login and password
    :type user: UserPassword

    :param user_db: user model from database
    :type user_db: User

    :return: is gotten password equal user's password
    :rtype: bool
    """
    return check_password_hash(user_db.password, user.password)


def remove_user(db: Session, user: UserModel) -> bool:
    """
    Marks user record in database as deleted and returns is_deleted.

    :param db: database session
    :type db: Session

    :param user: user model from database
    :type user: User

    :return: true if record is marked as deleted
    :rtype: bool
    """
    user.is_deleted = True
    db.commit()

    return user.is_deleted


def change_user_fields(db: Session, user: UserModel, new_fields: UserChange) -> UserModel:
    """
    Gets schema with user's new login and password and changes old values to new ones returning user model.

    :param db: database session
    :type db: Session

    :param user: user model from database
    :type user: User

    :param new_fields: schema with new login and password
    :type new_fields: UserChange

    :return: user model from database
    :rtype: UserModel
    """
    user.login = new_fields.new_login
    user.password = generate_password_hash(new_fields.new_password)
    db.commit()

    return user


def get_user(db: Session, id: int = None, login: str = None, token: str = None) -> Optional[UserModel]:
    """
    Gets and returns record from db table 'users' with one of gotten params: id, login or token.

    :param db: database session
    :type db: Session

    :param id: id of searching user
    :type id: int

    :param login: login of searching user
    :type login: str

    :param token: token of searching user
    :type token: str

    :return: user model from database if such exists
    :rtype: UserModel or None
    """
    db_user = None
    if id is not None:
        db_user = db.query(UserModel).filter_by(id=id, is_deleted=False).first()
    elif login is not None:
        db_user = db.query(UserModel).filter_by(login=login, is_deleted=False).first()
    elif token is not None:
        db_user = db.query(UserModel).filter_by(token=token, is_deleted=False).first()

    return db_user
