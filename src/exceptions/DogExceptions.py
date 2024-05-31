from src.exceptions.MyHTTPException import MyHTTPException


class NoDog(MyHTTPException):
    def __init__(self, id: int = None, name: str = None):
        detail = f"Dog with {'id' if name is None else 'name'} '{id if name is None else name}' doesn't exist"
        super(NoDog, self).__init__(detail)
