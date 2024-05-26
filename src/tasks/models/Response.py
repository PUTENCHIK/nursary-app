from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.database import BaseDBModel


class Response(BaseDBModel):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, unique=False, index=False)
    task_id = Column(Integer, unique=False, index=False)
    image_path = Column(String, unique=False, index=False)
    created_at = Column(DateTime, unique=False, index=False)
    is_confirmed = Column(Boolean, default=False, unique=False, index=False)
    confirmed_at = Column(DateTime, unique=False, index=False)
    is_deleted = Column(Boolean, default=False, unique=False, index=False)
