from src.tasks.schemas.TaskBase import TaskBase


class Task(TaskBase):
    collar_id: int
    text: str
