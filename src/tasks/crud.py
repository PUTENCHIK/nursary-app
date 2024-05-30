import datetime

from sqlalchemy.orm import Session
from typing import Optional

from src.tasks.models.Task import Task as TaskModel
from src.tasks.models.Response import Response as ResponseModel

from src.tasks.schemas.TaskAdd import TaskAdd
from src.tasks.schemas.ResponseAdd import ResponseAdd


def add_task(db: Session, task: TaskAdd, user_id: int) -> Optional[TaskModel]:
    db.task = TaskModel(
        author_id=user_id,
        collar_id=task.collar_id,
        text=task.text,
        created_at=datetime.datetime.now()
    )

    db.add(db.task)
    db.commit()
    db.refresh(db.task)

    return db.task


def add_response(db: Session, response: ResponseAdd, user_id: int) -> Optional[ResponseModel]:
    db.response = ResponseModel(
        author_id=user_id,
        task_id=response.task_id,
        image_path=response.image_path,
        created_at=datetime.datetime.now()
    )

    db.add(db.response)
    db.commit()
    db.refresh(db.response)

    return db.response


def confirm_response(db: Session, response: ResponseModel) -> bool:
    response.is_confirmed = True
    response.confirmed_at = datetime.datetime.now()
    db.commit()

    return response.is_confirmed


def remove_task(db: Session, task: TaskModel) -> bool:
    task.is_deleted = True
    db.commit()

    return task.is_deleted


def remove_response(db: Session, response: ResponseModel) -> bool:
    response.is_deleted = True
    db.commit()

    return response.is_deleted


def get_task(db: Session, task_id: int) -> Optional[TaskModel]:
    return db.query(TaskModel).filter_by(id=task_id, is_deleted=False).first()


def get_user_tasks(db: Session, author_id: int):
    return db.query(TaskModel).filter_by(author_id=author_id).all()


def get_response(db: Session,
                 response_id: int = None,
                 task_id: int = None,
                 is_confirmed: bool = None) -> Optional[ResponseModel]:
    if response_id is not None:
        return db.query(ResponseModel).filter_by(id=response_id).first()
    elif task_id is not None:
        if is_confirmed is None:
            return db.query(ResponseModel).filter_by(task_id=task_id).first()
        else:
            return db.query(ResponseModel).filter_by(task_id=task_id, is_confirmed=is_confirmed).first()


def get_confirmed_response(db: Session, task_id: int) -> Optional[ResponseModel]:
    return db.query(ResponseModel).filter_by(task_id=task_id, is_confirmed=True).first()


def is_task_active(db: Session, task: TaskModel) -> bool:
    db_response = get_response(db, task_id=task.id, is_confirmed=True)

    return db_response is not None
