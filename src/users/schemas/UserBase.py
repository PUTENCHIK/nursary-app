from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
