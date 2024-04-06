from sqlalchemy import Column, Integer, String, Boolean
from src.database import BaseDBModel


class User(BaseDBModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=False)
    is_admin = Column(Boolean, default=False, unique=False, index=False)
    is_deleted = Column(Boolean, default=False, unique=False, index=False)
