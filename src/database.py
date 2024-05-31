from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

db_url = "sqlite:///../src/nursary.db"

engine = create_engine(db_url, connect_args={"check_same_thread": False})

DBSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

BaseDBModel = declarative_base()
