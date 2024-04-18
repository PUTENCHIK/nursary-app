from sqlalchemy import Column, Integer, String, Boolean
from src.database import BaseDBModel


class Dog(BaseDBModel):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=False, index=False, default="Ralf")
    location = Column(String, unique=False, index=False, default="Unknown")
    is_deleted = Column(Boolean, default=False, unique=False, index=False)
