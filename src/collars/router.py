import re

from fastapi import APIRouter, Depends

from src.database import DBSession
from src.dependencies import get_db_session

from src.exceptions.DogException import DogException
from src.exceptions.CollarException import CollarException
from src.exceptions.ExploitException import ExploitException

from src.users.router import is_user_admin

from src.users.schemas.UserAuth import UserAuth

from src.collars.schemas.Dog import Dog
from src.collars.schemas.DogBase import DogBase
from src.collars.schemas.DogAdd import DogAdd

from src.collars.schemas.Collar import Collar
from src.collars.schemas.CollarBase import CollarBase
from src.collars.schemas.CollarAdd import CollarAdd
# from src.collars.schemas.CollarCoords import CollarCoords

from src.collars.schemas.Link import Link
from src.collars.schemas.Exploit import Exploit

from src.collars.crud import (
    add_dog as add_db_dog,
    get_dog as get_db_dog,
    add_collar as add_db_collar,
    get_collar as get_db_collar,
    link as add_link,
    get_exploit as get_db_exploit,
    remove_dog as remove_db_dog,
    remove_collar as remove_db_collar,
    unlink as remove_link,
    get_random_coords
)


collars_router = APIRouter()
router_name = "/collars"


@collars_router.post(f"{router_name}/add_dog", response_model=DogBase)
def add_dog(dog: DogAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    """
    Checks user is admin and if he is, add new dog to database.

    :param dog: schema with dog's name and description of its location
    :type dog: DogAdd

    :param user: schema with user's token
    :type user: UserAuth

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: id of new dog
    :rtype: DogBase

    :raises UserException
    """
    if is_user_admin(token=user.user_token, db=db):
        db_dog = add_db_dog(db, dog)
        return db_dog


@collars_router.post(f"{router_name}/add_collar", response_model=CollarBase)
def add_collar(collar: CollarAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    """
    Checks user is admin and if he is, add new collar to database.

    :param collar: schema with collar's code
    :type collar: CollarAdd

    :param user: schema with user's token
    :type user: UserAuth

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: id of new collar
    :rtype: CollarBase

    :raises UserException
    :raises CollarException
    """
    if is_user_admin(token=user.user_token, db=db):
        collar.code = collar.code.lower()
        if len(collar.code) != 6:
            raise CollarException.wrong_code_length()
        if re.search(r'^([a-z0-9]{6})$', collar.code) is None:
            raise CollarException.wrong_code()

        db_collar = add_db_collar(db, collar)
        return db_collar


@collars_router.post(f"{router_name}/link", response_model=bool)
async def link_dog_collar(link: Link, user: UserAuth, db: DBSession = Depends(get_db_session)):
    """
    Checks user is admin and dog and collar with gotten ids exist and if they do, will be added exploit record with
    date and time of creating.

    :param link: schema with collar's id and dog's i
    :type link: Link

    :param user: schema with user's token
    :type user: UserAuth

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: true if link was created
    :rtype: bool

    :raises UserException
    :raises CollarException
    :raises DogException
    :raises ExploitException
    """
    if is_user_admin(token=user.user_token, db=db):
        get_dog(link.dog_id, db)
        get_collar(link.collar_id, db)

        db_exploit = get_db_exploit(db, link.collar_id, link.dog_id)
        if db_exploit is not None:
            raise ExploitException.already_link(link.collar_id, link.dog_id)

        db_collar_exploit = get_db_exploit(db, collar_id=link.collar_id)
        if db_collar_exploit is not None:
            raise ExploitException.collar_already_linked(db_collar_exploit.collar_id, db_collar_exploit.dog_id)

        db_dog_exploit = get_db_exploit(db, dog_id=link.dog_id)
        if db_dog_exploit is not None:
            raise ExploitException.dog_already_linked(db_dog_exploit.dog_id, db_dog_exploit.collar_id)

        add_link(db, link)
        return True


@collars_router.post(f"{router_name}/remove_dog", response_model=bool)
def remove_dog(dog: DogBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    """
    Checks user is admin and dog exists. Then marks record of dog as deleted. If dog uses any collar, their link will
    be marked as ended.

    :param dog: schema with dog's id
    :type dog: DogBase

    :param user: schema with user's token
    :type user: UserAuth

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: true if dog was deleted
    :rtype: bool

    :raises UserException
    :raises DogException
    :raises ExploitException
    """
    if is_user_admin(token=user.user_token, db=db):
        db_dog = get_dog(dog.id, db)

        db_exploit = get_db_exploit(db, dog_id=dog.id)
        if db_exploit is not None:
            remove_link(db, db_exploit)

        return remove_db_dog(db, db_dog)


@collars_router.post(f"{router_name}/remove_collar", response_model=bool)
def remove_collar(collar: CollarBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    """
    Checks user is admin and collar exists. Then marks record of collar as deleted. If collar is used by any dog, their
    link will be marked as ended.

    :param collar: schema with collar's id
    :type collar: CollarBase

    :param user: schema with user's token
    :type user: UserAuth

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: true if collar was deleted
    :rtype: bool

    :raises UserException
    :raises CollarException
    :raises ExploitException
    """
    if is_user_admin(token=user.user_token, db=db):
        db_collar = get_collar(collar.id, db)

        db_exploit = get_db_exploit(db, collar_id=collar.id)
        if db_exploit is not None:
            remove_link(db, db_exploit)

        return remove_db_collar(db, db_collar)


@collars_router.post(f"{router_name}/unlink", response_model=bool)
def unlink_dog_collar(link: Link, user: UserAuth, db: DBSession = Depends(get_db_session)):
    """
    Checks dog, collar and link between them exist and user is admin. Then saves date and time of ending exploit.

    :param link: schema with collar's id and dog's i
    :type link: Link

    :param user: schema with user's token
    :type user: UserAuth

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: true if link was deleted
    :rtype: bool

    :raises UserException
    :raises CollarException
    :raises DogException
    :raises ExploitException
    """
    if is_user_admin(token=user.user_token, db=db):
        get_dog(link.dog_id, db)
        get_collar(link.collar_id, db)

        db_exploit = get_exploit(link.collar_id, link.dog_id, db)
        if db_exploit is None:
            ExploitException.no_exploit(link.collar_id, link.dog_id)

        return remove_link(db, db_exploit)


@collars_router.get(f"{router_name}/get_dog", response_model=Dog)
def get_dog(dog_id: int, db: DBSession = Depends(get_db_session)):
    """
    Returns database record from table 'dogs' with gotten id if such exists.

    :param dog_id: dog's id
    :type dog_id: int

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: schema with id, name and location of dog
    :rtype: Dog or None

    :raises DogException
    """
    db_dog = get_db_dog(db, dog_id)

    if db_dog is None:
        raise DogException.no_dog(id=dog_id)

    return db_dog


@collars_router.get(f"{router_name}/get_collar", response_model=Collar)
def get_collar(collar_id: int, db: DBSession = Depends(get_db_session)):
    """
    Returns database record from table 'collars' with gotten id if such exists.

    :param collar_id: collar's id
    :type collar_id: int

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: schema with id and code of collar
    :rtype: Collar or None

    :raises CollarException
    """
    db_collar = get_db_collar(db, collar_id)

    if db_collar is None:
        raise CollarException.no_collar(id=collar_id)

    return db_collar


@collars_router.get(f"{router_name}/get_coords")
def get_coords(collar_id: int, db: DBSession = Depends(get_db_session)):
    """
    Checks collar exists, and it is used by any dog. Then imitates getting current coordinates of dog.

    :param collar_id: collar's id
    :type collar_id: int

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: dict with latitude and longitude of collar
    :rtype: dict

    :raises CollarException
    :raises ExploitException
    """
    db_collar = get_collar(collar_id, db)
    db_exploit = get_exploit(collar_id=collar_id, db=db)
    if db_exploit is None:
        raise CollarException.cant_get_coords(collar_id)

    coords = get_random_coords(db_collar.code)

    return {
        "latitude": coords[0],
        "longitude": coords[1],
    }


@collars_router.get(f"{router_name}/get_link", response_model=Exploit)
def get_exploit(collar_id: int = None, dog_id: int = None, db: DBSession = Depends(get_db_session)):
    """
    Returns database record from table 'exploits' with gotten id either dog or collar or both if such exists.

    :param collar_id: collar's id
    :type collar_id: int

    :param dog_id: dog's id
    :type dog_id: int

    :param db: session for connecting to db
    :type db: sessionmaker

    :return: schema with collar's id, dog's id, date and time of start and end of exploit
    :rtype: Exploit

    :raises ExploitException
    """
    if collar_id is None and dog_id is None:
        raise ExploitException.no_both_ids()

    db_exploit = get_db_exploit(db, collar_id, dog_id)

    if db_exploit is None:
        raise ExploitException.no_exploit(collar_id, dog_id)

    return db_exploit
