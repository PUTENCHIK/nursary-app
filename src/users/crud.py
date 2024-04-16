from sqlalchemy.orm import Session
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

from src.users.models.User import User as UserModel
from src.users.schemas.UserPassword import UserPassword
from src.users.schemas.UserCreate import UserCreate
from src.users.schemas.UserToken import UserToken


def create_user(db: Session, user: UserCreate) -> Optional[UserModel]:
    # pwd = user.password[::-1]       # пока что по приколу меняем пароль
    pwd = generate_password_hash(user.password)

    db.user = UserModel(
        login=user.login,
        password=pwd,
        is_admin=(user.special_token is not None),
        is_deleted=False
    )

    db.add(db.user)
    db.commit()
    db.refresh(db.user)

    return db.user


def signin_user(user: UserPassword, user_db: UserModel) -> bool:
    return check_password_hash(user_db.password, user.password)


def remove_user(user: UserModel) -> bool:
    user.is_deleted = True
    return user.is_deleted


def change_user_fields(user: UserModel) -> UserModel:



def get_user(db: Session, id: int = None, login: str = None, token: str = None) -> Optional[UserModel]:
    db_user = None
    if id is not None:
        db_user = db.query(UserModel).filter(UserModel.id == id and not UserModel.is_deleted).first()
    elif login is not None:
        db_user = db.query(UserModel).filter(UserModel.login == login and not UserModel.is_deleted).first()
    elif token is not None:
        db_user = db.query(UserModel).filter(UserModel.token == token and not UserModel.is_deleted).first()

    return db_user
