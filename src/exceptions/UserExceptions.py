from src.exceptions.MyHTTPException import MyHTTPException


class UserAlreadyExists(MyHTTPException):
    def __init__(self, login: str):
        detail = f"User with login '{login}' is already exists"
        super(UserAlreadyExists, self).__init__(detail)


class WrongAdminToken(MyHTTPException):
    def __init__(self, token: str):
        detail = f"Entered wrong admin-token '{token}'"
        super(WrongAdminToken, self).__init__(detail)


class WrongPassword(MyHTTPException):
    def __init__(self, login: str):
        detail = f"Entered wrong password for login '{login}'"
        super(WrongPassword, self).__init__(detail)


class NoUser(MyHTTPException):
    def __init__(self, login: str = None, token: str = None):
        detail = f"No user with {'login' if token is None else 'token'} '{login if token is None else token}'"
        super(NoUser, self).__init__(detail)


class IsNotAdmin(MyHTTPException):
    def __init__(self, login: str = None, token: str = None):
        detail = f"User with {'login' if token is None else 'token'} '{login if token is None else token}' isn't admin"
        super(IsNotAdmin, self).__init__(detail)
