from pydantic import BaseModel


class UserAuth(BaseModel):
    user_token: str
