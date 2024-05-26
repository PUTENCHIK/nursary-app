from src.exceptions.MyHTTPException import MyHTTPException


class TaskException(MyHTTPException):
    @staticmethod
    def no_task(task_id: int):
        return TaskException.http(
            code=404,
            detail=f"Task with id '{task_id}' doesn't exist"
        )

    @staticmethod
    def unlinked_collar(collar_id: int):
        return TaskException.http(
            code=404,
            detail=f"Collar with id '{collar_id}' doesn't have any linked dog, so task can't be added to this collar"
        )

    @staticmethod
    def too_short_text():
        return TaskException.http(
            code=404,
            detail="Transmitted text must be longer than 10 symbols"
        )

    @staticmethod
    def cant_remove(task_id: int):
        return TaskException.http(
            code=404,
            detail=f"You can't remove not yours task with id '{task_id}'"
        )

    @staticmethod
    def has_responses(task_id: int):
        return TaskException.http(
            code=404,
            detail=f"Task with id '{task_id}' has responses and can't be removed"
        )
