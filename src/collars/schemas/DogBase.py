from pydantic import BaseModel


class DogBase(BaseModel):
    id: int
