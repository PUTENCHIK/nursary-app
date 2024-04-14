from src.users.schemas.UserBase import UserBase


class User(UserBase):
    id: int
    is_admin: bool
