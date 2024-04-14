from fastapi import HTTPException


class UserException(HTTPException):
    def __int__(self):
        self.status_code = 1000
        self.detail = "No detail"

    def http(self):
        return HTTPException(status_code=self.status_code, detail=self.detail)

    def user_exists(self, login: str):
        self.status_code = 1001
        self.detail = f"No user with login '{login}'."
