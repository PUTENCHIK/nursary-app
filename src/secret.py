from werkzeug.security import generate_password_hash, check_password_hash


def get_admin_token() -> str:
    secret_token = "toster123"
    return generate_password_hash(secret_token)


def check_admin_token(token: str) -> bool:
    return check_password_hash(get_admin_token(), token)
