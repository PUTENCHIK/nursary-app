from pydantic import BaseModel


class DogAdd(BaseModel):
    name: str
    location: str
