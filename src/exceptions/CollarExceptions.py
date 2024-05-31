from src.exceptions.MyHTTPException import MyHTTPException


class NoCollar(MyHTTPException):
    def __init__(self, id: int = None, code: str = None):
        detail = f"Collar with {'id' if code is None else 'code'} '{id if code is None else code}' doesn't exist"
        super(NoCollar, self).__init__(detail)


class ImpossibleGetCoordinates(MyHTTPException):
    def __init__(self, collar_id: int):
        detail = f"You can't get coords of collar with id '{collar_id}'s because it isn't linked with any dog"
        super(ImpossibleGetCoordinates, self).__init__(detail)


class WrongCodeLength(MyHTTPException):
    def __init__(self):
        detail = f"Length of collar's code must be 6 symbols"
        super(WrongCodeLength, self).__init__(detail)


class WrongCode(MyHTTPException):
    def __init__(self):
        detail = f"Collar's code must contain only numbers and latin letters"
        super(WrongCode, self).__init__(detail)


class CodeAlreadyAdded(MyHTTPException):
    def __init__(self, collar_code: str):
        detail = f"Code '{collar_code}' is already added into database"
        super(CodeAlreadyAdded, self).__init__(detail)
