import datetime

from sqlalchemy.orm import Session
from typing import Optional

from src.tasks.models.Task import Task as TaskModel
from src.tasks.models.Response import Response as ResponseModel

from src.tasks.schemas.TaskAdd import TaskAdd
from src.tasks.schemas.ResponseAdd import ResponseAdd


def add_task(db: Session, task: TaskAdd, user_id: int) -> Optional[TaskModel]:
    """
    Gets task's data from schema and adds database record.

    :param db: database session
    :type db: Session

    :param task: schema with collar's id and text of task
    :type task: TaskAdd

    :param user_id: user-creator's id
    :type user_id: int

    :return: new task model
    :rtype: TaskModel
    """
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
    """
    Gets response's data from schema and adds database record.

    :param db: database session
    :type db: Session

    :param response: schema with task's id and path of image
    :type response: ResponseAdd

    :param user_id: user-creator's id
    :type user_id: int

    :return: new response model
    :rtype: ResponseModel
    """
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
    """
    Marks response as confirmed and set date and time of confirming.

    :param db: database session
    :type db: Session

    :param response: response model
    :type response: ResponseModel

    :return: response's is_confirmed attribute
    :rtype: bool
    """
    response.is_confirmed = True
    response.confirmed_at = datetime.datetime.now()
    db.commit()

    return response.is_confirmed


def remove_task(db: Session, task: TaskModel) -> bool:
    """
    Marks task as deleted.

    :param db: database session
    :type db: Session

    :param task: task model
    :type task: TaskModel

    :return: task's is_deleted attribute
    :rtype: bool
    """
    task.is_deleted = True
    db.commit()

    return task.is_deleted


def remove_response(db: Session, response: ResponseModel) -> bool:
    """
    Marks response as deleted.

    :param db: database session
    :type db: Session

    :param response: response model
    :type response: ResponseModel

    :return: response's is_deleted attribute
    :rtype: bool
    """
    response.is_deleted = True
    db.commit()

    return response.is_deleted


def get_task(db: Session, task_id: int) -> Optional[TaskModel]:
    """
    Returns database record from table 'tasks' with gotten id if such exists.

    :param db: database session
    :type db: Session

    :param task_id: task's id
    :type task_id: int

    :return: task model if such exists
    :rtype: TaskModel or None
    """
    return db.query(TaskModel).filter_by(id=task_id, is_deleted=False).first()


def get_user_tasks(db: Session, author_id: int):
    """
    Returns list of tasks which author's id is equal gotten id.

    :param db: database session
    :type db: Session

    :param author_id: user's id
    :type author_id: int

    :return: list of task models.
    """
    return db.query(TaskModel).filter_by(author_id=author_id).all()


def get_response(db: Session,
                 response_id: int = None,
                 task_id: int = None,
                 is_confirmed: bool = None) -> Optional[ResponseModel]:
    """
    Returns database record from table 'responses' with gotten either response's id or task's. Also finds only confirmed
    response if param is_confirmed is true.

    :param db: database session
    :type db: Session

    :param response_id: response's id
    :type response_id: int or None

    :param task_id: task's id
    :type task_id: int or None

    :param is_confirmed: if is not None, it is necessary to check is_confirmed
    :type is_confirmed: bool or None

    :return: response model if such exists
    :rtype: ResponseModel or None
    """
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
