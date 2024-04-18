from sqlalchemy import Column, Integer, String, Boolean
from src.database import BaseDBModel


class Collar(BaseDBModel):
    __tablename__ = "collars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=False, index=False)
    is_deleted = Column(Boolean, default=False, unique=False, index=False)
