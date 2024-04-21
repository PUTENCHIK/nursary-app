from src.users.schemas.UserBase import UserBase


class UserCreate(UserBase):
    password: str
    is_admin: bool
    admin_token: str

    class Config:
        orm_mode = True
