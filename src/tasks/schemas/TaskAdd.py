from pydantic import BaseModel


class TaskAdd(BaseModel):
    collar_id: int
    text: str
