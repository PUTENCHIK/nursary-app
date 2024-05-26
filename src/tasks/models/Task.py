from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.database import BaseDBModel


class Task(BaseDBModel):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, unique=False, index=False)
    collar_id = Column(Integer, unique=False, index=False)
    text = Column(String, unique=False, index=False)
    created_at = Column(DateTime, unique=False, index=False)
    is_deleted = Column(Boolean, default=False, unique=False, index=False)
