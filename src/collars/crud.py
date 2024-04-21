from sqlalchemy.orm import Session
from typing import Optional

from src.collars.models.Dog import Dog as DogModel
from src.collars.schemas.DogAdd import DogAdd


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


def get_dog(db: Session, id: int) -> Optional[DogModel]:
    return db.query(DogModel).filter_by(id=id).first()
