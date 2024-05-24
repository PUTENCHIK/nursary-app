from src.exceptions.MyHTTPException import MyHTTPException


class CollarException(MyHTTPException):
    @staticmethod
    def no_collar(id: int = None, code: str = None):
        return CollarException.http(
            code=404,
            detail=f"Collar with {'id' if code is None else 'code'} '{id if code is None else code}' doesn't exist"
        )

