import datetime

from sqlalchemy.orm import Session
from typing import Optional

from src.dependencies import get_logger

from src.tasks.models.Task import Task as TaskModel
from src.tasks.models.Response import Response as ResponseModel

from src.tasks.schemas.TaskAdd import TaskAdd
from src.tasks.schemas.ResponseAdd import ResponseAdd


logger = get_logger('tasks_crud')


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
    :rtype: TaskModel or None
    """
    logger.add_debug("Adding task")

    db.task = TaskModel(
        author_id=user_id,
        collar_id=task.collar_id,
        text=task.text,
        created_at=datetime.datetime.now()
    )

    db.add(db.task)
    db.commit()
    db.refresh(db.task)

    logger.add_debug("Task created, returning instance")

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
    logger.add_debug("Adding response")

    db.response = ResponseModel(
        author_id=user_id,
        task_id=response.task_id,
        image_path=response.image_path,
        created_at=datetime.datetime.now()
    )

    db.add(db.response)
    db.commit()
    db.refresh(db.response)

    logger.add_debug("Response created, returning instance")

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
    logger.add_debug("Setting response is_confirmed as True")

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
    logger.add_debug("Setting task is_deleted as True")

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
    logger.add_debug("Setting response is_deleted as True")

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
    logger.add_debug("Getting task by id")

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
    logger.add_debug("Getting tasks for user")

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
    logger.add_debug(f"Getting response by {'response_id' if response_id is not None else 'task_id'}")

    if response_id is not None:
        return db.query(ResponseModel).filter_by(id=response_id).first()
    elif task_id is not None:
        if is_confirmed is None:
            return db.query(ResponseModel).filter_by(task_id=task_id).first()
        else:
            return db.query(ResponseModel).filter_by(task_id=task_id, is_confirmed=is_confirmed).first()
