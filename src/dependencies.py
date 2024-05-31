from src.database import DBSession


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
