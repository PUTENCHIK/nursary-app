from src.users.schemas.UserBase import UserBase


class UserPassword(UserBase):
    password: str

    class Config:
        orm_mode = True
