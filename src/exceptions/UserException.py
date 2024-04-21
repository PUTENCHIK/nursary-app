from src.exceptions.MyHTTPException import MyHTTPException


class UserException(MyHTTPException):
    @staticmethod
    def user_exists(login: str):
        return UserException.http(
            code=404,
            detail=f"User with login '{login}' is already exists."
        )

    @staticmethod
    def wrong_admin_token(token: str):
        return UserException.http(
            code=404,
            detail=f"Entered wrong admin-token '{token}'."
        )

    @staticmethod
    def wrong_password(login: str):
        return UserException.http(
            code=404,
            detail=f"Entered wrong password for login '{login}'."
        )

    @staticmethod
    def no_user(login: str = None, token: str = None):
        return UserException.http(
            code=404,
            detail=f"No user with {'login' if token is None else 'token'} '{login if token is None else token}'."
        )

    @staticmethod
    def is_not_admin(login: str = None, token: str = None):
        return UserException.http(
            code=404,
            detail=f"User with {'login' if token is None else 'token'} '{login if token is None else token}' isn't admin"
        )
