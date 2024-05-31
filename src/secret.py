from werkzeug.security import generate_password_hash, check_password_hash
from src.dependencies import get_logger


logger = get_logger('secret')


def get_admin_token() -> str:
    """
    Generates secret token which needed for registration admin accounts.

    :return: hashed admin token
    """
    logger.add_debug('Called function for hashing admin token')

    secret_token = "toster123"
    return generate_password_hash(secret_token)


def check_admin_token(token: str) -> bool:
    """
    Checks hashes of gotten token and admin token

    :param token: Gotten token from request
    :type token: str

    :return: boolean result of check
    """
    logger.add_debug('Called function for checking gotten admin token')

    return check_password_hash(get_admin_token(), token)
