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
    def __init__(self, id: int = None, login: str = None, token: str = None):
        detail = "No user with "
        if id is not None:
            detail += f"id = '{id}'"
        elif login is not None:
            detail += f"login = '{login}'"
        else:
            detail += f"token = '{token}'"

        super(NoUser, self).__init__(detail)


class IsNotAdmin(MyHTTPException):
    def __init__(self, id: int = None, login: str = None, token: str = None):
        detail = f"User with "
        if id is not None:
            detail += f"id '{id}'"
        elif login is not None:
            detail += f"login '{login}'"
        else:
            detail += f"token '{token}'"

        detail += " isn't admin"

        super(IsNotAdmin, self).__init__(detail)
