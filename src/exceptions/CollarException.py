from src.exceptions.MyHTTPException import MyHTTPException


class CollarException(MyHTTPException):
    @staticmethod
    def no_collar():
        pass
