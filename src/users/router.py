from fastapi import APIRouter, Depends, HTTPException

from src.database import DBSession
from src.dependencies import get_db_session
from schemas.User import User
from schemas.UserCreate import UserCreate
from crud import (
    create_user as create_db_user,
    get_user as get_db_user
)


user_router = APIRouter()


@user_router.post("/users/signup", response_model=User)
def create_user(user: UserCreate, db: DBSession = Depends(get_db_session)):
    if get_user(user.login, db):
        raise HTTPException(status_code=404, detail=f"User with login '{user.login}' is already exists.")
    return create_db_user(db, user)


@user_router.get("/users/get", response_model=User)
def get_user(login: str, db: DBSession = Depends(get_db_session)):
    db_user = get_db_user(db, login=login)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"No user with login '{login}'.")
    return db_user
