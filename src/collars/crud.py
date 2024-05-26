import datetime

from sqlalchemy.orm import Session
from typing import Optional

from src.collars.models.Dog import Dog as DogModel
from src.collars.models.Collar import Collar as CollarModel
from src.collars.models.Exploit import Exploit

from src.collars.schemas.DogAdd import DogAdd
from src.collars.schemas.CollarAdd import CollarAdd
from src.collars.schemas.Link import Link


def add_dog(db: Session, dog: DogAdd) -> Optional[DogModel]:
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
    db.collar = CollarModel(
        code=collar.code,
        is_deleted=False
    )

    db.add(db.collar)
    db.commit()
    db.refresh(db.collar)

    return db.collar


def link(db: Session, link: Link) -> Optional[Exploit]:
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
    dog.is_deleted = True
    db.commit()

    return dog.is_deleted


def remove_collar(db: Session, collar: CollarModel) -> bool:
    collar.is_deleted = True
    db.commit()

    return collar.is_deleted


def unlink(db: Session, exploit: Exploit) -> bool:
    exploit.end_exploit = datetime.datetime.now()
    db.commit()

    return True


def get_dog(db: Session, id: int) -> Optional[DogModel]:
    return db.query(DogModel).filter_by(id=id, is_deleted=False).first()


def get_collar(db: Session, id: int) -> Optional[CollarModel]:
    return db.query(CollarModel).filter_by(id=id, is_deleted=False).first()


def get_exploit(db: Session, collar_id: int = None, dog_id: int = None) -> Optional[Exploit]:
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
