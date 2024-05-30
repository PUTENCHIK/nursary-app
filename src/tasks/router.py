from fastapi import APIRouter, Depends

from src.database import DBSession
from src.dependencies import get_db_session

from src.exceptions.TaskException import TaskException
from src.exceptions.ResponseException import ResponseException

from src.users.router import get_user
from src.users.schemas.UserAuth import UserAuth

from src.collars.crud import get_exploit

from src.tasks.schemas.TaskBase import TaskBase
from src.tasks.schemas.TaskAdd import TaskAdd
from src.tasks.schemas.Task import Task
from src.tasks.schemas.ResponseBase import ResponseBase
from src.tasks.schemas.ResponseAdd import ResponseAdd
from src.tasks.schemas.Response import Response


from src.tasks.crud import (
    add_task as add_db_task,
    add_response as add_db_response,
    confirm_response as confirm_db_response,
    remove_task as remove_db_task,
    remove_response as remove_db_response,
    get_task as get_db_task,
    get_user_tasks,
    get_response as get_db_response,
    get_confirmed_response
)

tasks_router = APIRouter()
router_name = "/tasks"


@tasks_router.post(f"{router_name}/add_task", response_model=TaskBase)
def add_task(task: TaskAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    db_user = get_user(token=user.user_token, db=db)
    db_exploit = get_exploit(db, collar_id=task.collar_id)

    if db_exploit is None:
        raise TaskException.unlinked_collar(task.collar_id)

    if len(task.text) < 11:
        raise TaskException.too_short_text()

    return add_db_task(db, task, db_user.id)


@tasks_router.post(f"{router_name}/add_response", response_model=ResponseBase)
def add_response(response: ResponseAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    db_user = get_user(token=user.user_token, db=db)
    get_task(response.task_id, db)

    return add_db_response(db, response, db_user.id)


@tasks_router.post(f"{router_name}/confirm_response", response_model=bool)
def confirm_response(response: ResponseBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    db_user = get_user(token=user.user_token, db=db)
    db_response = get_response(response.id, db)
    db_task = get_task(db_response.task_id, db)

    if db_user.id != db_task.author_id:
        raise ResponseException.not_author(db_task.author_id, response.id, db_task.id)

    db_confirmed = get_confirmed_response(db, db_task.id)
    if db_confirmed is not None:
        if db_confirmed.id == response.id:
            raise ResponseException.already_confirmed(response.id)
        else:
            raise ResponseException.cant_confirm(db_task.id, db_confirmed.id)

    return confirm_db_response(db, db_response)


@tasks_router.post(f"{router_name}/remove_task", response_model=bool)
def remove_task(task: TaskBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    db_user = get_user(token=user.user_token, db=db)
    db_task = get_task(task.id, db)

    if db_user.id != db_task.author_id:
        raise TaskException.cant_remove(task.id)

    db_response = get_db_response(db, task_id=task.id)
    if db_response is not None:
        raise TaskException.has_responses(task.id)

    return remove_db_task(db, db_task)


@tasks_router.post(f"{router_name}/remove_response", response_model=bool)
def remove_response(response: ResponseBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    db_user = get_user(token=user.user_token, db=db)
    db_response = get_response(response.id, db)

    if db_user.id != db_response.author_id:
        raise ResponseException.cant_remove(response.id)

    return remove_db_response(db, db_response)


@tasks_router.get(f"{router_name}/get_task", response_model=Task)
def get_task(task_id: int, db: DBSession = Depends(get_db_session)):
    db_task = get_db_task(db, task_id)

    if db_task is None:
        raise TaskException.no_task(task_id)

    return db_task


@tasks_router.get(f"{router_name}/get_tasks", response_model=list[Task])
def get_tasks(author_id: int, db: DBSession = Depends(get_db_session)):
    return get_user_tasks(db, author_id)


@tasks_router.get(f"{router_name}/get_response", response_model=Response)
def get_response(response_id: int, db: DBSession = Depends(get_db_session)):
    db_response = get_db_response(db, response_id=response_id)

    if db_response is None:
        raise ResponseException.no_response(response_id)

    return db_response
