from src.database import DBSession
from src.logging.Logger import Logger


def get_db_session():
    """
    Creates DBSession and return it. Finally closes it.

    :return: None
    """
    session = DBSession()
    try:
        yield session
    finally:
        session.close()


def get_logger(name: str = "unkown") -> Logger:
    """
    Returns instance of Logger with gotten name.

    :param name: name of new logger
    :type name: str

    :return: logger with gotten name
    :rtype: Logger
    """
    logger = Logger(name)
    return logger
