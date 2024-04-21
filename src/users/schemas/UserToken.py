from src.users.schemas.User import User


class UserToken(User):
    token: str

    class Config:
        orm_mode = True
