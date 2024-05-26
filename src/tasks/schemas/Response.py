from src.tasks.schemas.ResponseBase import ResponseBase


class Response(ResponseBase):
    task_id: int
    image_path: str
