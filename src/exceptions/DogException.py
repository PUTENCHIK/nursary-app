from src.exceptions.MyHTTPException import MyHTTPException


class DogException(MyHTTPException):
    @staticmethod
    def no_dog(id: int = None, name: str = None):
        return DogException.http(
            code=404,
            detail=f"Dog with {'id' if name is None else 'name'} '{id if name is None else name}' doesn't exist"
        )
