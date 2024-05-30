from src.exceptions.MyHTTPException import MyHTTPException


class CollarException(MyHTTPException):
    @staticmethod
    def no_collar(id: int = None, code: str = None):
        return CollarException.http(
            code=404,
            detail=f"Collar with {'id' if code is None else 'code'} '{id if code is None else code}' doesn't exist"
        )

    @staticmethod
    def cant_get_coords(collar_id: int):
        return CollarException.http(
            code=404,
            detail=f"You can't get coords of collar with id '{collar_id}'s because it isn't linked with any dog"
        )

    @staticmethod
    def wrong_code_length():
        return CollarException.http(
            code=404,
            detail=f"Length of collar's code must be 6 symbols"
        )

    @staticmethod
    def wrong_code():
        return CollarException.http(
            code=404,
            detail=f"Collar's code must contain only numbers and latin letters"
        )
