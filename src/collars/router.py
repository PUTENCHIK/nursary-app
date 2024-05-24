from fastapi import APIRouter, Depends

from src.database import DBSession
from src.dependencies import get_db_session

from src.exceptions.DogException import DogException
from src.exceptions.CollarException import CollarException
from src.exceptions.ExploitException import ExploitException

from src.users.router import get_user, is_user_admin

from src.users.schemas.UserAuth import UserAuth

from src.collars.schemas.Dog import Dog
from src.collars.schemas.DogBase import DogBase
from src.collars.schemas.DogAdd import DogAdd

from src.collars.schemas.Collar import Collar
from src.collars.schemas.CollarBase import CollarBase
from src.collars.schemas.CollarAdd import CollarAdd

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
)


collars_router = APIRouter()
router_name = "/collars"


@collars_router.post(f"{router_name}/add_dog", response_model=DogBase)
def add_dog(dog: DogAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    if is_user_admin(token=user.user_token, db=db):
        db_dog = add_db_dog(db, dog)
        return db_dog


@collars_router.post(f"{router_name}/add_collar", response_model=CollarBase)
def add_collar(collar: CollarAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    if is_user_admin(token=user.user_token, db=db):
        db_collar = add_db_collar(db, collar)
        return db_collar


@collars_router.post(f"{router_name}/link", response_model=bool)
def link_dog_collar(link: Link, user: UserAuth, db: DBSession = Depends(get_db_session)):
    if is_user_admin(token=user.user_token, db=db):
        db_dog = get_dog(link.dog_id, db)
        db_collar = get_collar(link.collar_id, db)

        db_exploit = add_link(db, link)
        return True


@collars_router.post(f"{router_name}/remove_dog", response_model=bool)
def remove_dog(dog: DogBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    if is_user_admin(token=user.user_token, db=db):
        db_dog = get_dog(dog.id, db)

        return remove_db_dog(db, db_dog)


@collars_router.post(f"{router_name}/remove_collar", response_model=bool)
def remove_collar(collar: CollarBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    if is_user_admin(token=user.user_token, db=db):
        db_collar = get_collar(collar.id, db)

        return remove_db_collar(db, db_collar)


@collars_router.post(f"{router_name}/unlink", response_model=bool)
def unlink_dog_collar(link: Link, user: UserAuth, db: DBSession = Depends(get_db_session)):
    if is_user_admin(token=user.user_token, db=db):
        db_exploit = get_exploit(link.collar_id, link.dog_id, db)

        return remove_link(db, db_exploit)


@collars_router.get(f"{router_name}/get_dog", response_model=Dog)
def get_dog(dog_id: int, db: DBSession = Depends(get_db_session)):
    db_dog = get_db_dog(db, dog_id)

    if db_dog is None:
        raise DogException.no_dog(id=dog_id)

    return db_dog


@collars_router.get(f"{router_name}/get_collar", response_model=Collar)
def get_collar(collar_id: int, db: DBSession = Depends(get_db_session)):
    db_collar = get_db_collar(db, collar_id)

    if db_collar is None:
        raise CollarException.no_collar(id=collar_id)

    return db_collar


@collars_router.get(f"{router_name}/get_link", response_model=Exploit)
def get_exploit(collar_id: int, dog_id: int, db: DBSession = Depends(get_db_session)):
    db_exploit = get_db_exploit(db, collar_id, dog_id)

    if db_exploit is None:
        raise ExploitException.no_exploit(collar_id, dog_id)

    return db_exploit
