from sqlalchemy.orm import Session
from typing import Optional

from models.User import User as user_model
# from schemas.User import User as user_schema
from schemas.UserCreate import UserCreate
# from schemas.UserBase import UserBase


def create_user(db: Session, user: UserCreate) -> Optional[user_model]:
    pwd = user.password[::-1]       # пока что по приколу меняем пароль

    db.user = user_model(
        login=user.login,
        password=pwd,
        is_admin=(user.special_token is not None),
        is_deleted=False
    )

    db.add(db.user)
    db.commit()
    db.refresh(db.user)

    return db.user


def get_user(db: Session, id: int | None, login: str | None) -> Optional[user_model]:
    pass
