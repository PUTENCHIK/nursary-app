from src.users.schemas.User import User


class UserToken(User):
    token: str
