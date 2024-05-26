from pydantic import BaseModel


class ResponseAdd(BaseModel):
    task_id: int
    image_path: str
