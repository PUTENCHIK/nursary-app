from fastapi import APIRouter, Depends

from src.database import DBSession
from src.dependencies import get_db_session

from src.users.schemas.UserAuth import UserAuth

from src.tasks.schemas.TaskBase import TaskBase
from src.tasks.schemas.TaskAdd import TaskAdd

from src.tasks.schemas.ResponseBase import ResponseBase
from src.tasks.schemas.ResponseAdd import ResponseAdd


tasks_router = APIRouter()
router_name = "/tasks"


@tasks_router.post(f"{router_name}/add_task", response_model=TaskBase)
def add_task(task: TaskAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    pass


@tasks_router.post(f"{router_name}/add_response", response_model=ResponseBase)
def add_response(response: ResponseAdd, user: UserAuth, db: DBSession = Depends(get_db_session)):
    pass


@tasks_router.post(f"{router_name}/confirm_response", response_model=bool)
def confirm_response(response: ResponseBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    pass


@tasks_router.post(f"{router_name}/remove_task", response_model=bool)
def remove_task(task: TaskBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    pass


@tasks_router.post(f"{router_name}/remove_response", response_model=bool)
def remove_response(response: ResponseBase, user: UserAuth, db: DBSession = Depends(get_db_session)):
    pass
