from src.users.schemas.UserPassword import UserPassword


class UserChange(UserPassword):
    new_login: str
    new_password: str

    class Config:
        orm_mode = True
