from fastapi import FastAPI
from src.database import BaseDBModel, engine

from src.users.router import users_router
from src.collars.router import collars_router
from src.tasks.router import tasks_router


BaseDBModel.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)
app.include_router(collars_router)
app.include_router(tasks_router)


@app.get("/")
def root_greet():
    return {"message": "Hello on nursery-app!"}
