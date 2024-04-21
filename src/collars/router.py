from fastapi import APIRouter, Depends

from src.database import DBSession
from src.dependencies import get_db_session

from src.exceptions.DogException import DogException
from src.exceptions.CollarException import CollarException

from src.users.router import get_user, is_user_admin

from src.users.schemas.UserAuth import UserAuth
from src.collars.schemas.Dog import Dog
from src.collars.schemas.DogBase import DogBase
from src.collars.schemas.DogAdd import DogAdd

from src.collars.crud import (
    add_dog as add_db_dog,
    get_dog as get_db_dog
)


collars_router = APIRouter()
router_name = "/collars"


@collars_router.post(f"{router_name}/add_dog", response_model=DogBase)
async def add_dog(dog: DogAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    if is_user_admin(token=user.user_token):
        add_db_dog(db, dog)


@collars_router.post(f"{router_name}/add_collar")
def add_collar():
    pass


@collars_router.post(f"{router_name}/link")
def link_dog_collar():
    pass


@collars_router.post(f"{router_name}/remove_dog")
def remove_dog():
    pass


@collars_router.post(f"{router_name}/remove_collar")
def remove_collar():
    pass


@collars_router.post(f"{router_name}/unlink")
def unlink_dog_collar():
    pass


@collars_router.get(f"{router_name}/get_dog", response_model=Dog)
def get_dog(dog_id: int, db: DBSession = Depends(get_db_session)):
    db_dog = get_db_dog(db, dog_id)

    if db_dog is None:
        raise DogException.no_dog(id=dog_id)

    return db_dog
