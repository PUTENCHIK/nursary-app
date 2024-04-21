from pydantic import BaseModel


class UserBase(BaseModel):
    login: str

    class Config:
        orm_mode = True
