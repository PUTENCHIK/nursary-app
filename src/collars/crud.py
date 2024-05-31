import datetime
import random

from sqlalchemy.orm import Session
from typing import Optional

from src.collars.models.Dog import Dog as DogModel
from src.collars.models.Collar import Collar as CollarModel
from src.collars.models.Exploit import Exploit

from src.collars.schemas.DogAdd import DogAdd
from src.collars.schemas.CollarAdd import CollarAdd
from src.collars.schemas.Link import Link


def add_dog(db: Session, dog: DogAdd) -> Optional[DogModel]:
    """
    Gets dog's data from schema and adds database record.

    :param db: database session
    :type db: Session

    :param dog: schema with dog's name and location
    :type dog: DogAdd

    :return: new dog model
    :rtype: DogModel or None
    """
    db.dog = DogModel(
        name=dog.name,
        location=dog.location,
        is_deleted=False
    )

    db.add(db.dog)
    db.commit()
    db.refresh(db.dog)

    return db.dog


def add_collar(db: Session, collar: CollarAdd) -> Optional[CollarModel]:
    """
    Gets collar's data from schema and adds database record.

    :param db: database session
    :type db: Session

    :param collar: schema with collar's code
    :type collar: CollarAdd

    :return: new collar model
    :rtype: CollarModel or None
    """
    db.collar = CollarModel(
        code=collar.code,
        is_deleted=False
    )

    db.add(db.collar)
    db.commit()
    db.refresh(db.collar)

    return db.collar


def link(db: Session, link: Link) -> Optional[Exploit]:
    """
    Gets link's data from schema and adds database record.

    :param db: database session
    :type db: Session

    :param link: schema with collar's id and dog's id
    :type link: Link

    :return: new collar model
    :rtype: CollarModel or None
    """
    db.exploit = Exploit(
        collar_id=link.collar_id,
        dog_id=link.dog_id,
        start_exploit=datetime.datetime.now(),
        end_exploit=None
    )

    db.add(db.exploit)
    db.commit()
    db.refresh(db.exploit)

    return db.exploit


def remove_dog(db: Session, dog: DogModel) -> bool:
    """
    Marks gotten dog model as deleted.

    :param db: database session
    :type db: Session

    :param dog: dog model
    :type dog: DogModel

    :return: dog's is_deleted attribute
    :rtype: bool
    """
    dog.is_deleted = True
    db.commit()

    return dog.is_deleted


def remove_collar(db: Session, collar: CollarModel) -> bool:
    """
    Marks gotten collar model as deleted.

    :param db: database session
    :type db: Session

    :param collar: collar model
    :type collar: CollarModel

    :return: collar's is_deleted attribute
    :rtype: bool
    """
    collar.is_deleted = True
    db.commit()

    return collar.is_deleted


def unlink(db: Session, exploit: Exploit) -> bool:
    """
    Sets exploit model date and time of end of exploit.

    :param db: database session
    :type db: Session

    :param exploit: exploit model
    :type exploit: Exploit

    :return: true
    :rtype: bool
    """

    exploit.end_exploit = datetime.datetime.now()
    db.commit()

    return True


def get_dog(db: Session, id: int) -> Optional[DogModel]:
    """
    Returns database record from table 'dogs' with gotten id.

    :param db: database session
    :type db: Session

    :param id: dog's id
    :type id: int

    :return: dog model from database if such exists
    :rtype: DogModel or None
    """
    return db.query(DogModel).filter_by(id=id, is_deleted=False).first()


def get_collar(db: Session, id: int = None, code: str = None) -> Optional[CollarModel]:
    """
    Returns database record from table 'records' with gotten either id or code.

    :param db: database session
    :type db: Session

    :param id: collar's id
    :type id: int

    :param code: collar's code
    :type code: str

    :return: collar model from database if such exists
    :rtype: CollarModel or None
    """
    if id is not None:
        return db.query(CollarModel).filter_by(id=id, is_deleted=False).first()
    elif code is not None:
        return db.query(CollarModel).filter_by(code=code, is_deleted=False).first()


def get_exploit(db: Session, collar_id: int = None, dog_id: int = None) -> Optional[Exploit]:
    """
    Returns database record from table 'exploits' with gotten either collar's id or dog's id or both if such exists.

    :param db: database session
    :type db: Session

    :param collar_id: collar's id
    :type collar_id: int

    :param dog_id: dog's id
    :type dog_id: int

    :return: exploit model from database if such exists
    :rtype: Exploit or None
    """
    db_exploit = None

    if collar_id is not None and dog_id is not None:
        db_exploit = db.query(Exploit).filter_by(
            collar_id=collar_id,
            dog_id=dog_id,
            end_exploit=None,
        ).first()
    elif collar_id is not None:
        db_exploit = db.query(Exploit).filter_by(
            collar_id=collar_id,
            end_exploit=None,
        ).first()
    elif dog_id is not None:
        db_exploit = db.query(Exploit).filter_by(
            dog_id=dog_id,
            end_exploit=None,
        ).first()

    return db_exploit


def get_random_coords(collar_code: str) -> tuple[float, float]:
    """
    Generates random coordinates in format (latitude, longitude).

    :param collar_code: collar's code for getting its coordinates
    :type collar_code: str

    :return: tuple of 2 floats
    :rtype: tuple[float, float]
    """
    min_lat, max_lat = -90, 90
    min_lon, max_lon = -180, 180

    lat = min_lat + (max_lat-min_lat) * random.random()
    lon = min_lon + (max_lon-min_lon) * random.random()
    return lat, lon
