from fastapi import HTTPException


class UserExistsException(HTTPException):
    def __int__(self, user_login):
        super.__init__(status_code=1001, detail=f"No user with login '{user_login}'.")
