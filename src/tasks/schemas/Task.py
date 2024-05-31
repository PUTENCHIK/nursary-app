from src.tasks.schemas.TaskBase import TaskBase


class Task(TaskBase):
    collar_id: int
    author_id: int
    text: str

    class Config:
        orm_mod: True
