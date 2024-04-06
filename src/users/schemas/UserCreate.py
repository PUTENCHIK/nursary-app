from UserBase import UserBase


class UserCreate(UserBase):
    password: str
    special_token: str
