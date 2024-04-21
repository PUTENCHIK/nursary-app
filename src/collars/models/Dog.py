from sqlalchemy import Column, Integer, String, Boolean
from src.database import BaseDBModel


class Dog(BaseDBModel):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, index=False, default="Unknown")
    location = Column(String, unique=False, index=False, default="Unknown")
    is_deleted = Column(Boolean, unique=False, index=False, default=False)
