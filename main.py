from fastapi import FastAPI
from src.database import BaseDBModel, engine

from src.users.router import user_router

BaseDBModel.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)


@app.get("/")
def root_greet():
    return {"message": "Hello on nursery-app!"}


def special_token():
    return "toster123"