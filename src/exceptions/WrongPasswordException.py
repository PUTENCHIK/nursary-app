from fastapi import HTTPException


class WrongPasswordException(HTTPException):
    def __int__(self, user_login):
        super.__init__(status_code=1002, detail=f"Entered wrong password for login '{user_login}'.")
