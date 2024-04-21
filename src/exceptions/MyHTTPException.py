from fastapi import HTTPException


class MyHTTPException:
    @staticmethod
    def http(code: int, detail: str):
        return HTTPException(status_code=code, detail=detail)
