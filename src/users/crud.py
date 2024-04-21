from sqlalchemy.orm import Session
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex

from src.users.models.User import User as UserModel
from src.users.schemas.UserPassword import UserPassword
from src.users.schemas.UserCreate import UserCreate
from src.users.schemas.UserToken import UserToken
from src.users.schemas.UserChange import UserChange


def create_user(db: Session, user: UserCreate) -> Optional[UserModel]:
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
    return check_password_hash(user_db.password, user.password)


def remove_user(db: Session, user: UserModel) -> bool:
    user.is_deleted = True
    db.commit()

    return user.is_deleted


def change_user_fields(db: Session, user: UserModel, new_fields: UserChange) -> UserModel:
    user.login = new_fields.new_login
    user.password = generate_password_hash(new_fields.new_password)
    db.commit()

    return user


def get_user(db: Session, id: int = None, login: str = None, token: str = None) -> Optional[UserModel]:
    db_user = None
    if id is not None:
        db_user = db.query(UserModel).filter_by(id=id, is_deleted=False).first()
    elif login is not None:
        db_user = db.query(UserModel).filter_by(login=login, is_deleted=False).first()
    elif token is not None:
        db_user = db.query(UserModel).filter_by(token=token, is_deleted=False).first()

    return db_user
