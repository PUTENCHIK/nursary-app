from pydantic import BaseModel


class Link(BaseModel):
    collar_id: int
    dog_id: int
