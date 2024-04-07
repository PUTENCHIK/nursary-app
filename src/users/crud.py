from sqlalchemy.orm import Session
from typing import Optional

from src.users.models.User import User as UserModel
from src.users.schemas.UserPassword import UserPassword
from src.users.schemas.UserCreate import UserCreate


def create_user(db: Session, user: UserCreate) -> Optional[UserModel]:
    pwd = user.password[::-1]       # пока что по приколу меняем пароль

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
    pwd = user.password[::-1]

    return pwd == user_db.password


def remove_user(db: Session, user: UserPassword) -> bool:
    db_user = get_user(db, login=user.login)
    db_user.is_deleted = True
    return True


def get_user(db: Session, id: int = None, login: str = None) -> Optional[UserModel]:
    if id is not None:
        db_user = db.query(UserModel).filter(UserModel.id == id).first()
        return db_user
    if login is not None:
        db_user = db.query(UserModel).filter(UserModel.login == login).first()
        return db_user
    return None
